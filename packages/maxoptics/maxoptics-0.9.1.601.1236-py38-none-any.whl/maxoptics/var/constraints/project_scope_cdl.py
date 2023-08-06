# flake8: noqa F405

from typing import Union

from maxoptics.core.base.BaseContainer import WaveformShell
from maxoptics.core.component.base.Component import Solver
from maxoptics.core.error import ProjectBuildError
from maxoptics.core.logger import info_print as info_p
from maxoptics.core.project.ProjectBase import get_component_with_class as gcc
from maxoptics.core.project.ProjectBase import get_component_with_type as gct
from maxoptics.macros import (
    PortLeftAttach,
    PortRightAttach,
    X_Normal,
    get_namespace,
)
from maxoptics.var.constraints.project_checks import (
    isin,
    project_pre_run,
    project_pre_save,
)
from maxoptics.var.constraints.utils import assert_f, raise_error
from maxoptics.var.models.MitM import *  # noqa
from maxoptics.var.MosIO import MaxOptics
from maxoptics.var.project import MosProject


def info_print(*args, **kwargs):
    if Config.Verbose:
        info_p(*args, **kwargs)


def sync_waveform_attributes(
    project: MosProject, component: Union[ModeSource, FDTDPortGroup]
):
    """Sync a component's waveform-related attribute with attributes recorded in its waveform.
    The waveform must be at waveform.attrs.waveform_id.
    The waveform can be an int or a WaveformShell object.

    Args:
        project (MosProject): The project.
        component (ModeSource|FDTDPortGroup): The component.

    Returns:
        None
    """
    if hasattr(component, "attrs"):
        waveform = component.attrs.waveform_id
        if isinstance(waveform, int):
            client: MaxOptics = project.__parent__
            __waveforms = client.user_waveforms.all()
            __waveforms_id = client.user_waveforms.ids
            __ind = __waveforms_id.index(waveform)
            __waveform = __waveforms[__ind]  # Overwrite waveform

        elif isinstance(waveform, WaveformShell):
            __waveform = waveform

        else:
            raise ProjectBuildError(
                component, "type of waveform_id is {}".format(type(waveform))
            )

        sync_dict = dict(
            wavelength_center=__waveform.center_wavelength,
            wavelength=__waveform.center_wavelength,
            waveform_name=__waveform.center_wavelength,
            wavelength_max=__waveform.wavelength_stop,
            wavelength_min=__waveform.wavelength_start,
        )

        for key, val in sync_dict.items():
            if key in component and component["key"] != val:
                info_print(f"{component}: {key} = {val}")
                component[key] = val


# %% Post Add Component
ret = [
    (
        ("ProjectAddSolver",),
        lambda p, c: gct(c.type.name, p)[1],
        lambda p, c: raise_error(ValueError("Duplicated solvers are added")),
    ),
    (
        ("ProjectAddFDTDPort",),
        lambda p, c: not gct(c.type.name, p)[1],  # The first Port
        lambda p, c: (
            port_group := gcc(FDTDPortGroup, p)[1],
            info_print(f"{port_group.name}: source_port={c.id}"),
            port_group.attrs.update(source_port=c.id),
        ),
    ),
    (
        ("ProjectAddMonitor",),
        lambda p, c: True,
        lambda p, c: (
            solver := gcc(Solver, p)[1],
            solver
            or raise_error(
                ValueError(
                    "Please add solver before you start to add monitor!"
                )
            ),
        ),
    ),
    (
        ("ProjectAddSweep",),
        lambda p, c: True,
        lambda p, c: (
            solver := gcc(Solver, p)[1],
            assert_f(solver, "Solver is not added"),
            solver_name := solver.__class__.__name__.lower(),
            solver_repr := {"fdtd": 0, "eme": 1}[solver_name],
            info_print(f"{c.name}: solver = {solver_repr}"),
            c.attrs.set("solver", solver_repr),
            info_print(f"project.DOCUMENT: sweep[{solver_name}] = [{c}]"),
            p.DOCUMENT.attrs.sweep.set(solver_name, [c]),
        ),
    ),
    (
        ("ProjectAddMatrixSweep",),
        lambda p, c: True,
        lambda p, c: (
            solver := gcc(Solver, p)[1],
            assert_f(solver, "Solver is not added"),
            solver_name := solver.__class__.__name__.lower(),
            info_print(f"project.DOCUMENT: sweep[{solver_name}] = [{c}]"),
            p.DOCUMENT.attrs.sweep.set(solver_name, [c]),
        ),
    ),
    (
        ("ProjectAddEmePort",),
        lambda p, c: True,
        lambda p, c: (
            eme := gcc(EME, p)[1],
            eme
            or raise_error(
                ValueError(
                    "Please add EME solver before you start to add port!"
                )
            ),
            updated := dict(
                port_location=c.attrs.port_location,
                y=eme.attrs.y,
                y_span=eme.attrs.y_span,
                z=eme.attrs.z,
                z_span=eme.attrs.z_span,
            ),
            info_print(
                "{c.name}: port_location = {port_location}, y = {y}, "
                "y_span = {y_span}, z = {z}, z_span = {z_span}".format(
                    c=c, **updated
                )
            ),
            c.update(**updated),
        ),
    ),
    (
        ("ProjectAddProfileMonitor",),
        lambda p, c: True,
        lambda p, c: (
            eme := gcc(EME, p)[1],
            eme
            or raise_error(
                ValueError(
                    "Please add EME solver before you add ProfileMonitor!"
                )
            ),
        ),
    ),
    (
        (
            "ProjectAddModeExpansion",
            "ProjectAddPowerMonitor",
            "ProjectAddTimeMonitor",
        ),
        lambda p, c: True,
        lambda p, c: (
            fdtd := gcc(FDTD, p)[1],
            fdtd
            or raise_error(
                ValueError(
                    f"Please add FDTD solver before you add {c.type.name}!"
                )
            ),
        ),
    ),
    (
        ("ProjectAddIndexMonitor",),
        lambda _, __: True,
        lambda p, c: (
            solver := gcc((FDTD, EME), p)[1],
            solver
            or raise_error(
                ProjectBuildError(
                    IndexMonitor, "You need add EME or FDTD first"
                )
            ),
        ),
    ),
]

# %% Pre Save/Run methods
ret += [
    (
        ("ProjectPreSave",),
        lambda _, __: True,
        lambda p, _: project_pre_save(p),
    ),
    (
        ("ProjectPreRun",),
        lambda p, c: True,
        lambda p, task_type: project_pre_run(p, task_type),
    ),
]

# %% Pre-Post Set attribute methods
ret += [
    (
        ("EmePortPostSet__port_location",),
        lambda _, __: True,
        lambda p, c: (
            eme := gcc(EME, p)[1],
            port_location := c.attrs.port_location,
            assert_f(
                port_location in [PortLeftAttach, PortRightAttach],
                f"Parameter port_location should be in [{PortLeftAttach},{PortRightAttach}]",
            ),
            updated := dict(
                x_span=0,
                x=eme.attrs.x_max
                if port_location == PortRightAttach
                else eme.attrs.x_min,
            ),
            info_print("{c.name}: x_span = 0, x = {x}".format(c=c, **updated)),
            c.update(**updated),
        ),
    ),
    # (
    #     ("IndexMonitorPostSet__monitor_type",),
    #     lambda _, __: True,
    #     lambda p, c: (
    #         eme := gcc(EME, p)[1],
    #         eme
    #         and c.attrs.monitor_type
    #         not in X_Normal(get_namespace("IndexMonitorAttrs"))
    #         and raise_error(
    #             ProjectBuildError(
    #                 IndexMonitor,
    #                 f"Index Monitor in EME project can only be x-normal (monitor_type={X_Normal})",
    #             )
    #         ),
    #     ),
    # ),
    # (
    #     ("...PostSet__waveform_id",),
    #     lambda _, __: True,
    #     lambda p, c: (None, sync_waveform_attributes(p, c)),
    # ),
    # (
    #     (
    #         "ModeExpansionTypeAttrsMonitor_settingPostSet__...",
    #         "PowerMonitorAttrsMonitor_settingPostSet__...",
    #         "IndexMonitorAttrsMonitor_settingPostSet__...",
    #     ),
    #     lambda _, __: True,
    #     lambda p, c: (
    #         info_print(f"{c.__class__.__name__}: override_global_options = 1"),
    #         c.__parent_ref__().set("override_global_options", 1),
    #     ),
    # ),
]
