# flake8: noqa
import uuid
from functools import singledispatchmethod
from typing import Literal

from attr import asdict, define, field

from .meta import ArcWaveguide as __ArcWaveguide
from .meta import BezierCurve as __BezierCurve
from .meta import Charge as __Charge
from .meta import Circle as __Circle
from .meta import Constant as __Constant
from .meta import CustomPolygon as __CustomPolygon
from .meta import Document as __Document
from .meta import EME as __EME
from .meta import Electrical as __Electrical
from .meta import Ellipse as __Ellipse
from .meta import EmePort as __EmePort
from .meta import FDE as __FDE
from .meta import FDTD as __FDTD
from .meta import FDTDPort as __FDTDPort
from .meta import FDTDPortGroup as __FDTDPortGroup
from .meta import Fiber as __Fiber
from .meta import GdsPolygon as __GdsPolygon
from .meta import GlobalMonitor as __GlobalMonitor
from .meta import IndexMonitor as __IndexMonitor
from .meta import LinearTrapezoid as __LinearTrapezoid
from .meta import MatrixSweep as __MatrixSweep
from .meta import Mesh as __Mesh
from .meta import ModeExpansion as __ModeExpansion
from .meta import ModeSource as __ModeSource
from .meta import PowerMonitor as __PowerMonitor
from .meta import ProfileMonitor as __ProfileMonitor
from .meta import Rectangle as __Rectangle
from .meta import Region as __Region
from .meta import Ring as __Ring
from .meta import SCurve as __SCurve
from .meta import Sector as __Sector
from .meta import Sweep as __Sweep
from .meta import TimeMonitor as __TimeMonitor
from .meta import Triangle as __Triangle
from ..config import Config
from ...core.abc import ExportableAttrS
from ...core.utils import ShadowAttr


class Sweep(__Sweep):
    def get_component_options(self):
        project = self.__parent_ref__()
        solver = project.solver
        if isinstance(solver, EME):
            return [{"label": "S", "value": "S"}]
        elif isinstance(solver, FDTD):
            return [
                {"label": "T", "value": "T"},
                {"label": "H", "value": "H"},
                {"label": "E", "value": "E"},
                {"label": "Hx", "value": "Hx"},
                {"label": "Hy", "value": "Hy"},
                {"label": "Hz", "value": "Hz"},
                {"label": "Ex", "value": "Ex"},
                {"label": "Ey", "value": "Ey"},
                {"label": "Ez", "value": "Ez"},
                {"label": "Energy Density", "value": "Energy Density"},
                {"label": "Px", "value": "Px"},
                {"label": "Py", "value": "Py"},
                {"label": "Pz", "value": "Pz"},
            ]
        else:
            raise NotImplementedError(
                "Only support parameter sweep on EME and FDTD !"
            )

    def append_result_monitor(self, name: str, monitor, component: str):
        @define
        class SweepResult(ExportableAttrS):
            resultComponent = field(converter=str)
            resultName = field(converter=str)
            resultObject = field(converter=str)
            id = field(default=str(uuid.uuid4()))
            componentOptions = field(default=self.get_component_options())

        if isinstance(monitor, str):
            self.attrs.resultList.append(
                asdict(SweepResult(component, name, monitor))
            )
        else:
            self.attrs.resultList.append(
                asdict(SweepResult(component, name, monitor.id))
            )

    @singledispatchmethod
    def append_param_data(self):
        pass

    @append_param_data.register
    def _(
        self,
        name: str,
        start: float,
        end: float,
        points_num: int,
        _type: str = "number",
    ):
        def not_null(instance, attribute, value):
            if not value:
                raise ValueError(f"SweepParam can't be named as {_}")

        @define
        class SweepParamRangeData(ExportableAttrS):
            start = field(converter=float)
            end = field(converter=float)
            pointAmount = field(converter=int)
            paramName = field(converter=str, validator=not_null)
            type = field(converter=str)
            id = str(uuid.uuid4())

            @property
            def export(self):
                base_dikt = asdict(self)
                diff = (self.end - self.start) / (self.pointAmount - 1)
                values = list(
                    self.start + i * diff for i in range(self.pointAmount)
                )
                append_dikt = {
                    f"value{i + 1}": values[i] for i in range(self.pointAmount)
                }
                return {**base_dikt, **append_dikt}

        self.attrs.paramData.append(
            SweepParamRangeData(
                start=start,
                end=end,
                pointAmount=points_num,
                paramName=name,
                type=_type,
            )
        )
        self.attrs.pointsNum = str(points_num)

    @append_param_data.register
    def _(
        self,
        lst: list,
        name: str,
        _type: str = "number",
    ):
        def not_null(instance, attribute, value):
            if not value:
                raise ValueError(f"SweepParam can't be named as {_}")

        @define
        class SweepParamValueData(ExportableAttrS):
            values: list = field(converter=tuple)
            paramName = field(converter=str, validator=not_null)
            type = field(converter=str)
            start = field(converter=float, default=0)
            end = field(converter=float, default=0)
            id = str(uuid.uuid4())

            @property
            def export(self):
                pointAmount = len(self.values)

                base_dikt = asdict(self)
                base_dikt.pop("values")
                base_dikt["pointAmount"] = pointAmount

                values = sorted(self.values)
                append_dikt = {
                    f"value{i + 1}": values[i] for i in range(pointAmount)
                }

                return {**base_dikt, **append_dikt}

        self.attrs.paramData.append(
            SweepParamValueData(values=lst, paramName=name, type=_type)
        )

    def list_params_name(self):
        return [name for _ in self.attrs.paramData if (name := _["paramName"])]


class Document(__Document):
    def append_global_param(
        self,
        name: str,
        expression="",
        default_value: float = "0",
        description: str = "",
    ):
        def not_null(instance, attribute, value):
            if not value:
                raise ValueError(f"SweepParam can't be named as {_}")

        @define
        class SweepParamData:
            globleParamKey = field(converter=str)
            globleParamExp = field(converter=str)
            globleParamValue = field()
            globleParamDes = field(converter=str)

        self.attrs.configGlobleParam.append(
            asdict(
                SweepParamData(name, expression, default_value, description)
            )
        )


class ArcWaveguide(__ArcWaveguide):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class BezierCurve(__BezierCurve):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Charge(__Charge):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Circle(__Circle):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Constant(__Constant):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class CustomPolygon(__CustomPolygon):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Electrical(__Electrical):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Ellipse(__Ellipse):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class EME(__EME):
    # TODO: Not safe
    def append_cell(
        self,
        span=10,
        cell_num=5,
        number_of_modes=10,
        sc=0,
        fix: Literal["x", "x_min", "x_max"] = "x",
    ):
        assert fix in ["x", "x_min", "x_max"], "Invalid input!"
        cell_group = self.attrs.cell_group
        cell_group.append(
            {
                "span": span,
                "cell_num": cell_num,
                "number_of_modes": number_of_modes,
                "sc": sc,
            }
        )

        span = sum(_["span"] for _ in cell_group)
        if fix == "x":
            pass
        elif fix == "x_min":
            self.attrs.x = self[fix] + span / 2
        elif fix == "x_max":
            self.attrs.x = self[fix] - span / 2

        self.attrs.x_span = span


class EmePort(__EmePort):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class FDE(__FDE):
    dx = ShadowAttr("dxd")
    dy = ShadowAttr("dyd")
    dz = ShadowAttr("dzd")

    def __init__(self, project_ref):
        super().__init__(project_ref)


class FDTD(__FDTD):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class FDTDPort(__FDTDPort):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class FDTDPortGroup(__FDTDPortGroup):
    waveform = ShadowAttr("waveform_id")

    def __init__(self, project_ref):
        super().__init__(project_ref)


class Fiber(__Fiber):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class GdsPolygon(__GdsPolygon):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class GlobalMonitor(__GlobalMonitor):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class IndexMonitor(__IndexMonitor):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class LinearTrapezoid(__LinearTrapezoid):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class MatrixSweep(__MatrixSweep):
    def append_table_data(self, port, mode=1, active=True):
        project = self.__parent_ref__()
        self.attrs.tableData.append(
            {
                "index": project.ports.index(port),
                "isActive": active,
                "mode": mode,
                "port": port.name,
                "portId": port.id,
            }
        )


class Mesh(__Mesh):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class ModeExpansion(__ModeExpansion):
    def append_monitor_for_mode_expansion(
        self, monitor: "PowerMonitor", name="me"
    ):
        assert isinstance(monitor, PowerMonitor)

        self.attrs.monitors_for_expansion.append(
            {
                "id": monitor.id,
                "index": len(self.attrs.monitors_for_expansion),
                "name": name,
            }
        )

        if monitor.attrs.override_global_options:
            Config.DisableConstraints = True
            for key, val in monitor.attrs.monitor_setting.to_dict().items():
                if key in self:
                    self.set(key, val)
            Config.DisableConstraints = False

        self.sync_spatial(monitor)
        return self

    def __init__(self, project_ref):
        super().__init__(project_ref)


class ModeSource(__ModeSource):
    waveform = ShadowAttr("waveform_id")

    def __init__(self, project_ref):
        super().__init__(project_ref)


class PowerMonitor(__PowerMonitor):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class ProfileMonitor(__ProfileMonitor):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Rectangle(__Rectangle):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Region(__Region):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Ring(__Ring):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class SCurve(__SCurve):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Sector(__Sector):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class TimeMonitor(__TimeMonitor):
    def __init__(self, project_ref):
        super().__init__(project_ref)


class Triangle(__Triangle):
    def __init__(self, project_ref):
        super().__init__(project_ref)
