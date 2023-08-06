import inspect
from functools import lru_cache
from typing import Dict

import attr
import yaml

from maxoptics.core.abc import Exportable


@lru_cache(maxsize=1)
def namespace():
    from maxoptics.var.config import BASEDIR

    nf = BASEDIR / "var" / "models" / "namespace.yml"
    with open(nf, "r") as f:
        __namespace = yaml.load(f, Loader=yaml.SafeLoader)
    return __namespace


def get_namespace(klass_name, ns=None):
    if ns is None:
        ns = {}

    __namespace = namespace()
    if klass_name in __namespace:
        ret = __namespace[klass_name]
        return {key.replace("-", "_"): val for key, val in ret.items()}
    else:
        return ns


@attr.define
class Macro(Exportable):
    name: str = attr.field(repr=True)
    __namespace__: Dict = attr.field(default={}, repr=False)

    @property
    def export(self):
        try:
            return self.__namespace__[self.name]
        except KeyError as e:
            from maxoptics.core.logger import error_print

            error_print(
                f"Unknown macro in the context: {e}, \ncontext: {self.__namespace__}"
            )
            from maxoptics.core.error import ProjectBuildError

            return ProjectBuildError(
                Macro, f"{self.name} not in {self.__namespace__}"
            )

    def to_dict(self, *args, **kwargs):
        return self

    def __contains__(self, item):
        return item in [self.export, self.__class__(self.name)]

    def __call__(self, ns):
        return self.__class__(self.name, ns)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.name == other.name


def _():
    name = inspect.stack()[1][4][0].split("=")[0].strip()
    return Macro(name)


Point = _()
X_Linear = _()
Y_Linear = _()
Z_Linear = _()
XYZ_3D = _()
X_Normal = _()
Y_Normal = _()
Z_Normal = _()

PortLeftAttach = 0
PortRightAttach = 1

# TaskTypes

Simu_Index_Monitor = "INDEX_MONITOR"
Simu_FDE = "FDE"
Simu_FDE_Sweep = "FDE_SWEEP"
Simu_EME_FDE = "EME_FDE"
Simu_EME_EME = "EME_EME"
Simu_EME_Wavelength_Sweep = "EME_SWEEP"
Simu_EME_Propagation_Sweep = "EME_SWEEP"
Simu_EME_Parameter_Sweep = "EME_SWEEP_PARAMS"
Simu_FDTD = "FDTD"
Simu_FDTD_Parameter_Sweep = "FDTD_SWEEP"
Simu_FDTD_Smatrix = "FDTD_SMATRIX"
Simu_FDTD_Mode_Expansion = "MODE_EXPANSION"
Simu_PD = "PD"
Simu_Modulator = "SIMODULATOR"

Simu_Types = (
    Simu_FDE,
    Simu_FDE_Sweep,
    Simu_EME_FDE,
    Simu_EME_EME,
    Simu_EME_Wavelength_Sweep,
    Simu_EME_Propagation_Sweep,
    Simu_EME_Parameter_Sweep,
    Simu_FDTD,
    Simu_FDTD_Parameter_Sweep,
    Simu_FDTD_Smatrix,
    Simu_FDTD_Mode_Expansion,
    Simu_PD,
    Simu_Modulator,
    Simu_Index_Monitor,
)
# TaskStatus

TaskDone = 2
TaskRunning = 1
TaskWaiting = 0
TaskFailed = -2
TaskInterrupt = -1
