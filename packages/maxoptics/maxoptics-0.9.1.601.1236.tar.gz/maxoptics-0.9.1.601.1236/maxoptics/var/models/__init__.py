# coding=utf-8
from typing import TypeVar
from uuid import uuid4
from weakref import ref

from ...core.utils.currying import fast_currying
from .MitM import (
    EME,
    FDE,
    FDTD,
    ArcWaveguide,
    BezierCurve,
    Charge,
    Circle,
    Constant,
    CustomPolygon,
    Document,
    Electrical,
    Ellipse,
    EmePort,
    FDTDPort,
    FDTDPortGroup,
    Fiber,
    GdsPolygon,
    GlobalMonitor,
    IndexMonitor,
    LinearTrapezoid,
    MatrixSweep,
    Mesh,
    ModeExpansion,
    ModeSource,
    PowerMonitor,
    ProfileMonitor,
    Rectangle,
    Region,
    Ring,
    SCurve,
    Sector,
    Sweep,
    TimeMonitor,
    Triangle,
)

T = TypeVar("T")


@fast_currying
def append_arc_waveguide(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `ArcWaveguide`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = ArcWaveguide(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_bezier_curve(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `BezierCurve`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = BezierCurve(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_charge(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Charge`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Charge(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_circle(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Circle`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Circle(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_constant(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Constant`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Constant(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_custom_polygon(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `CustomPolygon`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = CustomPolygon(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_document(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Document`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Document(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_electrical(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Electrical`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Electrical(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_ellipse(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Ellipse`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Ellipse(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_eme(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `EME`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = EME(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_eme_port(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `EmePort`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = EmePort(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_fde(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `FDE`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = FDE(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_fdtd(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `FDTD`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = FDTD(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_fdtd_port(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `FDTDPort`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = FDTDPort(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_fdtd_port_group(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `FDTDPortGroup`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = FDTDPortGroup(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_fiber(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Fiber`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Fiber(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_gds_polygon(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `GdsPolygon`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = GdsPolygon(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_global_monitor(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `GlobalMonitor`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = GlobalMonitor(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_index_monitor(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `IndexMonitor`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = IndexMonitor(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_linear_trapezoid(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `LinearTrapezoid`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = LinearTrapezoid(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_matrix_sweep(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `MatrixSweep`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = MatrixSweep(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_mesh(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Mesh`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Mesh(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_mode_expansion(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `ModeExpansion`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = ModeExpansion(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_mode_source(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `ModeSource`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = ModeSource(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_power_monitor(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `PowerMonitor`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = PowerMonitor(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_profile_monitor(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `ProfileMonitor`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = ProfileMonitor(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_rectangle(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Rectangle`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Rectangle(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_region(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Region`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Region(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_ring(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Ring`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Ring(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_s_curve(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `SCurve`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = SCurve(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_sector(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Sector`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Sector(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_sweep(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Sweep`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Sweep(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_time_monitor(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `TimeMonitor`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = TimeMonitor(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


@fast_currying
def append_triangle(project: T, **kwargs) -> T:
    r"""Insert a component to project.

    Args:
        project (ProjectCore): The Project.

        \*\*kwargs: The attributes which will be absorbed by created `Triangle`.

    Returns:
        ProjectCore: return the project.
    """
    project_ref = ref(project)

    res = Triangle(project_ref)
    res.id = uuid4().__str__()
    res.update(**kwargs)
    res.name = kwargs["name"]

    project.attach_component(res, res.name)
    return project


class MosProjectAccessory:
    def create_arc_waveguide(
        self, name="ArcWaveguide", **kwargs
    ) -> ArcWaveguide:
        return next(
            reversed(
                append_arc_waveguide(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_bezier_curve(self, name="BezierCurve", **kwargs) -> BezierCurve:
        return next(
            reversed(
                append_bezier_curve(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_charge(self, name="Charge", **kwargs) -> Charge:
        return next(
            reversed(
                append_charge(self, name=name, **kwargs).components.values()
            )
        )

    def create_circle(self, name="Circle", **kwargs) -> Circle:
        return next(
            reversed(
                append_circle(self, name=name, **kwargs).components.values()
            )
        )

    def create_constant(self, name="Constant", **kwargs) -> Constant:
        return next(
            reversed(
                append_constant(self, name=name, **kwargs).components.values()
            )
        )

    def create_custom_polygon(
        self, name="CustomPolygon", **kwargs
    ) -> CustomPolygon:
        return next(
            reversed(
                append_custom_polygon(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_document(self, name="Document", **kwargs) -> Document:
        return next(
            reversed(
                append_document(self, name=name, **kwargs).components.values()
            )
        )

    def create_electrical(self, name="Electrical", **kwargs) -> Electrical:
        return next(
            reversed(
                append_electrical(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_ellipse(self, name="Ellipse", **kwargs) -> Ellipse:
        return next(
            reversed(
                append_ellipse(self, name=name, **kwargs).components.values()
            )
        )

    def create_eme(self, name="EME", **kwargs) -> EME:
        return next(
            reversed(append_eme(self, name=name, **kwargs).components.values())
        )

    def create_eme_port(self, name="EmePort", **kwargs) -> EmePort:
        return next(
            reversed(
                append_eme_port(self, name=name, **kwargs).components.values()
            )
        )

    def create_fde(self, name="FDE", **kwargs) -> FDE:
        return next(
            reversed(append_fde(self, name=name, **kwargs).components.values())
        )

    def create_fdtd(self, name="FDTD", **kwargs) -> FDTD:
        return next(
            reversed(
                append_fdtd(self, name=name, **kwargs).components.values()
            )
        )

    def create_fdtd_port(self, name="FDTDPort", **kwargs) -> FDTDPort:
        return next(
            reversed(
                append_fdtd_port(self, name=name, **kwargs).components.values()
            )
        )

    def create_fdtd_port_group(
        self, name="FDTDPortGroup", **kwargs
    ) -> FDTDPortGroup:
        return next(
            reversed(
                append_fdtd_port_group(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_fiber(self, name="Fiber", **kwargs) -> Fiber:
        return next(
            reversed(
                append_fiber(self, name=name, **kwargs).components.values()
            )
        )

    def create_gds_polygon(self, name="GdsPolygon", **kwargs) -> GdsPolygon:
        return next(
            reversed(
                append_gds_polygon(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_global_monitor(
        self, name="Global Monitor", **kwargs
    ) -> GlobalMonitor:
        if hasattr(self, "global_monitor"):
            self.global_monitor.update(**kwargs)
            return self.global_monitor

        else:
            return next(
                reversed(
                    append_global_monitor(
                        self, name=name, **kwargs
                    ).components.values()
                )
            )

    def create_index_monitor(
        self, name="IndexMonitor", **kwargs
    ) -> IndexMonitor:
        return next(
            reversed(
                append_index_monitor(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_linear_trapezoid(
        self, name="LinearTrapezoid", **kwargs
    ) -> LinearTrapezoid:
        return next(
            reversed(
                append_linear_trapezoid(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_matrix_sweep(self, name="MatrixSweep", **kwargs) -> MatrixSweep:
        return next(
            reversed(
                append_matrix_sweep(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_mesh(self, name="Mesh", **kwargs) -> Mesh:
        return next(
            reversed(
                append_mesh(self, name=name, **kwargs).components.values()
            )
        )

    def create_mode_expansion(
        self, name="ModeExpansion", **kwargs
    ) -> ModeExpansion:
        return next(
            reversed(
                append_mode_expansion(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_mode_source(self, name="ModeSource", **kwargs) -> ModeSource:
        return next(
            reversed(
                append_mode_source(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_power_monitor(
        self, name="PowerMonitor", **kwargs
    ) -> PowerMonitor:
        return next(
            reversed(
                append_power_monitor(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_profile_monitor(
        self, name="ProfileMonitor", **kwargs
    ) -> ProfileMonitor:
        return next(
            reversed(
                append_profile_monitor(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_rectangle(self, name="Rectangle", **kwargs) -> Rectangle:
        return next(
            reversed(
                append_rectangle(self, name=name, **kwargs).components.values()
            )
        )

    def create_region(self, name="Region", **kwargs) -> Region:
        return next(
            reversed(
                append_region(self, name=name, **kwargs).components.values()
            )
        )

    def create_ring(self, name="Ring", **kwargs) -> Ring:
        return next(
            reversed(
                append_ring(self, name=name, **kwargs).components.values()
            )
        )

    def create_s_curve(self, name="SCurve", **kwargs) -> SCurve:
        return next(
            reversed(
                append_s_curve(self, name=name, **kwargs).components.values()
            )
        )

    def create_sector(self, name="Sector", **kwargs) -> Sector:
        return next(
            reversed(
                append_sector(self, name=name, **kwargs).components.values()
            )
        )

    def create_sweep(self, name="Sweep", **kwargs) -> Sweep:
        return next(
            reversed(
                append_sweep(self, name=name, **kwargs).components.values()
            )
        )

    def create_time_monitor(self, name="TimeMonitor", **kwargs) -> TimeMonitor:
        return next(
            reversed(
                append_time_monitor(
                    self, name=name, **kwargs
                ).components.values()
            )
        )

    def create_triangle(self, name="Triangle", **kwargs) -> Triangle:
        return next(
            reversed(
                append_triangle(self, name=name, **kwargs).components.values()
            )
        )
