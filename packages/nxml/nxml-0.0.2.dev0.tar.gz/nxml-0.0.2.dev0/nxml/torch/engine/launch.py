# Source code modified from https://github.com/facebookresearch/detectron2
#
# Copyright (c) Facebook, Inc. and its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import Callable, Tuple, Union, Optional

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from datetime import timedelta

import torch
from torch import distributed as dist
from torch import multiprocessing as mp
from torch.distributed import Backend

from . import comm


__all__ = [
    "DEFAULT_TIMEOUT",
    "launch",
]


DEFAULT_TIMEOUT = timedelta(minutes=1)
AUTO = Literal["auto"]


def _get_free_port():
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding to port 0 will cause the OS to find an available port for us
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()

    # NOTE: there is still a chance the port could be taken by other processes.
    return port


def launch(
    fn: Callable,
    args: Tuple = (),
    num_machines: int = 1,
    machine_rank: int = 0,
    num_local_devices: Union[int, AUTO] = 1,
    init_method: Optional[Union[str, AUTO]] = "auto",
    backend: Backend = Backend.NCCL,
    start_method: str = "spawn",
    timeout: timedelta = DEFAULT_TIMEOUT,
) -> None:

    if num_local_devices == "auto" or num_local_devices == -1:
        assert num_machines == 1, 'num_local_devices = "auto" not supported in multi-machine jobs.'
        num_local_devices = torch.cuda.device_count()

    world_size = num_machines * num_local_devices

    if world_size > 1:
        if init_method == "auto":
            assert num_machines == 1, 'init_method = "auto" not supported in multi-machine jobs.'
            init_method = f"tcp://localhost:{_get_free_port()}"

        if num_machines > 1 and init_method.startswith("file://"):
            logger = logging.getLogger(__name__)
            logger.warning("file:// is not a reliable in multi-machine jobs. Prefer tcp://")

        try:
            mp.spawn(
                _mp_launcher,
                nprocs=num_local_devices,
                args=(fn, args, world_size, machine_rank, num_local_devices, init_method, backend, timeout),
                daemon=False,
                start_method=start_method,
            )
        except KeyboardInterrupt:
            print("Interrupted")
        except Exception as e:
            raise e  # TODO: add exception handling

    else:
        try:
            fn(*args)
        except KeyboardInterrupt:
            print("Interrupted")
        except Exception as e:
            raise e  # TODO: add exception handling


def _mp_launcher(
    local_rank: int,
    fn: Callable,
    args: Tuple,
    world_size: int,
    machine_rank: int,
    num_local_devices: int,
    init_method: str,
    backend: Backend = Backend.NCCL,
    timeout: timedelta = DEFAULT_TIMEOUT,
) -> None:

    assert torch.cuda.is_available(), "cuda is not available. Please check your installation."

    try:
        dist.init_process_group(
            backend=backend,
            init_method=init_method,
            world_size=world_size,
            rank=(machine_rank * num_local_devices + local_rank),
            timeout=timeout,
        )
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Process group init: {init_method}")
        raise e

    available_local_devices = torch.cuda.device_count()

    if num_local_devices > available_local_devices:
        raise RuntimeError(
            f"Requested {num_local_devices} local devices, "
            f"but only {available_local_devices} local devices are available."
        )

    torch.cuda.set_device(local_rank)

    # Setup the local process group (which contains ranks within the same machine)
    assert comm._LOCAL_PROCESS_GROUP is None

    num_machines = world_size // num_local_devices

    for i in range(num_machines):
        ranks_on_i = list(range(i * num_local_devices, (i + 1) * num_local_devices))
        pg = dist.new_group(ranks_on_i)
        if i == machine_rank:
            comm._LOCAL_PROCESS_GROUP = pg

    # synchronize is needed here to prevent a possible timeout after calling init_process_group
    # See: https://github.com/facebookresearch/maskrcnn-benchmark/issues/172
    comm.synchronize()

    fn(*args)
    # try:
    # except KeyboardInterrupt:
    #     pass
    # except Exception as e:
    #     raise e  # TODO: add exception handling

    # dist.destroy_process_group()
