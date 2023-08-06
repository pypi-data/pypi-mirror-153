from typing import Type

import yaml
from attr import define, asdict, field

from maxoptics.core.component.base.Component import ProjectComponent
from maxoptics.macros import (
    Simu_FDE,
    Simu_FDTD,
    Simu_EME_EME,
    Simu_FDTD_Mode_Expansion,
)
from maxoptics.var.MosIO import WhaleClients


@define
class TinyTaskInfo:
    id: int
    handler: Type
    tarsrc_name: str = field(default=None)

    def get_task(self, monitor, config):
        if isinstance(monitor, ProjectComponent):
            project = monitor.__parent_ref__()
        else:
            project = None
        return self.handler(self.id, project, config, 2, self.tarsrc_name)

    def to_dict(self):
        return asdict(self)


class Workspace:
    def __init__(self):
        self.main = TinyTaskInfo(0, WhaleClients)
        self.main_task_type: str = ""
        self.others = {
            Simu_FDE: {},
            Simu_EME_EME: {},
            Simu_FDTD: {},
            Simu_FDTD_Mode_Expansion: {},
            "source_modes": {},
        }

    def load(self, path):
        with open(path, "r") as f:
            dikt = yaml.unsafe_load(f)
            self.__dict__ = dikt
        return self

    def dump(self, path):
        with open(path, "w") as f:
            yaml.dump(self.__dict__, f)
