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

from enum import Enum
from typing import Callable, Tuple, Union, Optional
from datetime import timedelta

from torch import distributed as dist
from torch import multiprocessing as mp


__all__ = [
    "DEFAULT_TIMEOUT",
    "launch",
]


DEFAULT_TIMEOUT = timedelta(seconds=30)


class Devices(Enum):
    AUTO = "auto"


class StartMethod(Enum):
    SPAWN = "spawn"
    FORK = "fork"



def launch(
    fn: Callable,
    args: Tuple,
    num_machines: int = 1,
    machine_rank: int = 0,
    num_local_devices: Union[int, Devices] = 1,
    dist_url: Optional[str] = None,
    timeout: timedelta = DEFAULT_TIMEOUT,
) -> None:
    pass


# TODO
