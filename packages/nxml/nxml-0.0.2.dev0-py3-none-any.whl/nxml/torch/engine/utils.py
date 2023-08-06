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

from typing import Union

from torch.nn import Module
from torch.nn.parallel import DistributedDataParallel

from .comm import get_world_size, get_local_rank


__all__ = [
    "create_ddp_model",
]


def create_ddp_model(
    model: Module,
    *,
    device_ids = None,
    # fp16_compression=False,
    **kwargs,
) -> Union[Module, DistributedDataParallel]:
    """
    Create a DistributedDataParallel model if there are >1 processes.

    Args:
        model: a torch.nn.Module
        kwargs: other arguments of :module:`torch.nn.parallel.DistributedDataParallel`.
    """

    if get_world_size() == 1:
        return model

    if device_ids is None:
        device_ids = [get_local_rank()]

    ddp = DistributedDataParallel(model, device_ids, **kwargs)

    # if fp16_compression:
    #     from torch.distributed.algorithms.ddp_comm_hooks import default as comm_hooks
    #     ddp.register_comm_hook(state=None, hook=comm_hooks.fp16_compress_hook)

    return ddp
