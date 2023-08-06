import os.path
from math import inf, floor
from typing import List

from maxoptics import X_Normal
from maxoptics.core.abc import Exportable
from maxoptics.core.base.BaseContainer import WaveformShell
from maxoptics.core.component.base.Component import ProjectComponent
from maxoptics.core.error import ProjectBuildError
from maxoptics.core.logger import info_print, warn_print
from maxoptics.core.project.ProjectBase import (
    yield_components_with_class,
    get_component_with_class,
)
from maxoptics.macros import (
    get_namespace,
    Y_Normal,
    Z_Normal,
    Simu_Index_Monitor,
)
from maxoptics.var.MosIO import MaxOptics
from maxoptics.var.models import (
    EmePort,
    FDTDPort,
    FDTD,
    FDE,
    EME,
    ModeExpansion,
    PowerMonitor,
    IndexMonitor,
    FDTDPortGroup,
)
from maxoptics.var.project import MosProject


def isin(o1, o2):
    if round(o1.attrs.x_min, 10) < round(o2.attrs.x_min, 10):
        return False, f"{o1.attrs.x_min} < {o2.attrs.x_min}"
    if round(o1.attrs.y_min, 10) < round(o2.attrs.y_min, 10):
        return False, f"{o1.attrs.y_min} < {o2.attrs.y_min}"
    if round(o1.attrs.z_min, 10) < round(o2.attrs.z_min, 10):
        return False, f"{o1.attrs.z_min} < {o2.attrs.z_min}"
    if round(o1.attrs.x_max, 10) > round(o2.attrs.x_max, 10):
        return False, f"{o1.attrs.x_max} < {o2.attrs.x_max}"
    if round(o1.attrs.y_max, 10) > round(o2.attrs.y_max, 10):
        return False, f"{o1.attrs.y_max} < {o2.attrs.y_max}"
    if round(o1.attrs.z_max, 10) > round(o2.attrs.z_max, 10):
        return False, f"{o1.attrs.z_max} < {o2.attrs.z_max}"
    return True, ""


def project_pre_save(project: MosProject):
    with info_print("Pre-save checking..."):
        components = project.components.values()
        components_types = [
            c.type.name for c in components if isinstance(c, ProjectComponent)
        ]

        __check_global_monitor(components_types, project)

        solver = project.solver

        if solver:
            if isinstance(solver, FDE):
                with info_print("Checking FDE..."):
                    namespace = get_namespace("FDEAttrs")

                    if solver.attrs.solver_type in X_Normal(namespace):
                        info_print("x_span = 0")
                        solver.attrs.x_span = 0
                        solver.attrs.define_x_mesh = 0

                    elif solver.attrs.solver_type in Y_Normal(namespace):
                        info_print("y_span = 0")
                        solver.attrs.y_span = 0
                        solver.attrs.define_y_mesh = 0

                    elif solver.attrs.solver_type in Z_Normal(namespace):
                        info_print("z_span = 0")
                        solver.attrs.z_span = 0
                        solver.attrs.define_z_mesh = 0
                    else:
                        raise ProjectBuildError(
                            solver,
                            f"solver_type is {solver.attrs.solver_type}",
                        )

            if isinstance(solver, EME):
                for _, mo in yield_components_with_class(
                    IndexMonitor, project
                ):
                    if mo.attrs.monitor_type not in X_Normal(
                        get_namespace("IndexMonitorAttrs")
                    ):
                        raise ProjectBuildError(
                            IndexMonitor,
                            f"Index Monitor in EME project can only be x-normal (monitor_type={X_Normal})",
                        )

            if isinstance(solver, FDTD):
                __check_monitor_mode_expansion_created(project)
                __check_mode_expansion_monitor_fit(project)
                __check_port_group(project)

        __check_mode_index(project)
        __check_materials_and_waveforms(project)


def __check_mode_index(project: MosProject):
    for comp in project.sources + project.ports:
        with info_print("Checking mode_index..."):
            if hasattr(comp.attrs, "mode_index"):
                assert isinstance(comp.attrs.mode_index, int)


# %% project_pre_save
def __check_global_monitor(components_types, project):
    info_print("Checking Global Monitor...", end="")
    if "GlobalMonitor" not in components_types and project.type == "passive":
        project.add("GlobalMonitor")
        warn_print("Missing!")
    else:
        print("Done!")


def __check_monitor_mode_expansion_created(project: MosProject):
    info_print("Checking Power Monitors' mode_expansion...")
    for i, (name, pm) in enumerate(
        yield_components_with_class(PowerMonitor, project)
    ):
        has_me = pm.attrs.mode_expansion
        if has_me and not has_me.get("__used__"):
            mode_expansion = project.create_mode_expansion(
                f"ModeExpansionFor{pm.name}"
            )
            for _i in range(i + 1):
                mode_expansion.append_monitor_for_mode_expansion(
                    pm, name=pm.name + f"({_i})"
                )

            for key, val in has_me.items():
                if key in mode_expansion.attrs:
                    mode_expansion.attrs[key] = val
            has_me["__used__"] = mode_expansion.name
            info_print(f"ModeExpansionFor{pm.name} Added.")


def __check_mode_expansion_monitor_fit(project: MosProject):
    info_print("Checking Mode Expansion and Power Monitor...", end="")
    for name, me in yield_components_with_class(ModeExpansion, project):
        monitors_info: List[PowerMonitor] = me.attrs.monitors_for_expansion
        for monitor_info in monitors_info:
            monitor_id = monitor_info["id"]
            monitors_id = [_.id for _ in project.monitors]
            assert monitor_id in monitors_id, (
                f"{me.name}'s monitors_for_expansion "
                f"include a unknown monitor id: {monitor_id}\n"
                f"not in {monitors_id}"
            )

            ind = monitors_id.index(monitor_id)
            monitor = project.monitors[ind]
            for attr in ["x", "x_span", "y", "y_span", "z", "z_span"]:
                moa = monitor.attrs[attr]
                mea = me.attrs[attr]
                assert (
                    mea == moa
                ), f"{me.name} and {monitor.name} {attr} not fix: {mea} != {moa}"
    print("Done!")


def __check_materials_and_waveforms(project: MosProject):
    info_print("Checking Materials and Waveforms...", end="")
    components = project.components
    for name, component in components.items():
        material = component.get("materialId", silent=True) or component.get(
            "background_material", silent=True
        )
        if material == 0:
            raise ProjectBuildError(name, "materialId is 0")

        waveform = component.get("waveform_id", silent=True)
        if waveform == 0:
            raise ProjectBuildError(name, "waveform_id is 0")
    print("Done!")


def __check_port_group(project: MosProject):
    info_print("Checking Port Group...", end="")
    _, pg = get_component_with_class(FDTDPortGroup, project)
    if pg:
        source_port = pg.attrs.source_port
        if isinstance(source_port, Exportable):
            pg.attrs.source_port = source_port.id
        elif isinstance(source_port, str):
            pass
        else:
            raise ProjectBuildError(pg, f"get source_port: {source_port}")

    print("Done!")


# %%


def project_pre_run(project: MosProject, task_type):
    """Pre run checking. Check about source, port and monitor settings.

    Args:
        project (MosProject): The project.
        task_type (str): The task type.

    Returns:
        None
    """
    with info_print("Pre-run checking..."):
        # Checks with side effect
        # Save
        project.save(check=False)
        __project_check_modeFileName(project, project.__parent__.user_id)
        __project_check_source(project, task_type)
        __project_check_monitor(project)
        __project_check_port(project, task_type)
        project.save()


def __project_check_modeFileName(project: MosProject, user_id):
    for _ in project.ports + project.sources:
        if _.attrs.mode_selection == 4:
            if _.attrs.modeFileName == "":
                raise ProjectBuildError(
                    _, "mode_selection is User Import but modeFileName == ''"
                )
            elif (
                "/" in _.attrs.modeFileName or "\\" in _.attrs.modeFileName
            ) and os.path.isfile(_.attrs.modeFileName):
                raise ProjectBuildError(
                    _,
                    "You should input a filename rather than path to a local file. "
                    "If you haven't uploaded your file, "
                    "you can use UserImport (from maxoptics.var.visualizer) to upload your file.",
                )
            elif not _.attrs.modeFileName.startswith(f"{user_id}/"):
                new_name = f"{user_id}/" + _.attrs.modeFileName
                warn_print(f"{_.name}.attrs.modeFileName = {new_name}")
                _.attrs.modeFileName = new_name


# %% project_pre_run
def __project_check_monitor(project: MosProject):
    """Check whether there are out-of-region monitors."""
    solver = project.solver
    global_monitor = project.global_monitor

    def get_waveform(component):
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
        return __waveform

    wmin = min(
        [
            *[
                wav.wavelength_start
                for _ in project.sources + project.port_groups
                if (wav := get_waveform(_))
            ],
            inf,
        ]
    )

    wmax = max(
        [
            *[
                wav.wavelength_stop
                for _ in project.sources + project.port_groups
                if (wav := get_waveform(_))
            ],
            -inf,
        ]
    )

    for mon in project.monitors:
        with info_print(f"Checking {mon.name}..."):
            with info_print("Checking region..."):
                in_, err = isin(mon, solver)
                if in_ is False:
                    raise ProjectBuildError(
                        mon,
                        f"Monitor {mon.name} is out of simulation region!, {err}",
                    )

            with info_print("Checking override_global_options..."):
                if hasattr(mon.attrs, "override_global_options"):
                    if not mon.attrs.override_global_options:
                        if hasattr(
                            mon.attrs, "override_global_monitor_settings"
                        ):
                            for (
                                key,
                                val,
                            ) in global_monitor.attrs.export.items():
                                settings = (
                                    mon.attrs.override_global_monitor_settings
                                )
                                if key in settings and settings[key] != val:
                                    info_print(
                                        f"{key} = {val}. Old value is {settings[key]}"
                                    )
                                    mon.attrs.override_global_monitor_settings.set(
                                        key, val
                                    )
                        mon.attrs.override_global_options = 0

            with info_print("Checking use_source_limits..."):
                if hasattr(mon.attrs, "use_source_limits"):
                    if mon.attrs.use_source_limits:
                        if wmin != inf and wmax != -inf:
                            if mon.attrs["wavelength_min"] != wmin:
                                info_print(
                                    f"wavelength_min = {wmin}. Old value is {mon.attrs['wavelength_min']}"
                                )
                                mon.attrs["wavelength_min"] = wmin
                            if mon.attrs["wavelength_max"] != wmax:
                                info_print(
                                    f"wavelength_max = {wmax}. Old value is {mon.attrs['wavelength_max']}"
                                )
                                mon.attrs["wavelength_max"] = wmax

                        else:
                            warn_print(
                                f"The source wavelength range is {wmin} - {wmax}"
                            )


def __project_check_source(project: MosProject, task_type: str):
    sources = project.sources2
    mesh_ret = project.recalc_mesh(task_type)
    if mesh_ret["code"] != 11000 and "msg" in mesh_ret:
        solver = project.solver
        mesh_ret = project.recalc_mesh(solver.type.name)

    sol_attrs = project.solver.attrs
    if (
        (dx := mesh_ret.get("dx"))
        and (dy := mesh_ret.get("dy"))
        and (dz := mesh_ret.get("dz"))
    ):
        if isinstance(project.solver, FDTD):
            project.solver.attrs.dx_arr = dx
            project.solver.attrs.dy_arr = dy
            project.solver.attrs.dz_arr = dz
            # Global monitor
            dt = mesh_ret["time"]["dt"]
            gm = project.global_monitor
            gma = gm.attrs
            gma.desired_sampling = (
                gma.min_sampling_per_cycle * gma.frequency_max
            )
            gma.nyquist_limit = 3.5 * gma.frequency_max
            gma.down_sample_time = (
                floor(1 / (dt * gma.nyquist_limit * 1e12)) if dt else 0
            )
            gma.actual_sampling = (
                1 / (dt * gma.down_sample_time * 1e12) if dt else 0
            )

            for _, mon in yield_components_with_class(PowerMonitor, project):
                mset = mon.attrs.monitor_setting
                mset.desired_sampling = (
                    mset.min_sampling_per_cycle * mset.frequency_max
                )
                mset.nyquist_limit = 3.5 * mset.frequency_max
                mset.down_sample_time = (
                    floor(1 / (dt * mset.nyquist_limit * 1e12)) if dt else 0
                )
                mset.actual_sampling = (
                    1 / (dt * mset.down_sample_time * 1e12) if dt else 0
                )

        def layer_number(dr, roof_floor):
            try:
                return mesh_ret["spatial_characteristics"][
                    "boundary_conditions"
                ][f"{dr}_{roof_floor}"]["condition"]["cpml"]["layer_number"]
            except Exception:
                return 0

        def layer_thick(_direction, _minmax):
            nonlocal dx, dy, dz

            d = eval(f"d{_direction}")
            ln = layer_number(_direction, _minmax)
            if ln == 0:
                return 0
            else:
                _ = min(ln, len(d))
                if _minmax == "min":
                    return sum(d[:_])
                elif _minmax == "max":
                    return -(sum(d[-_:]))
                else:
                    assert False

        simu_region = dict(
            x_max=sol_attrs.x_max + layer_thick("x", "max"),
            x_min=sol_attrs.x_min + layer_thick("x", "min"),
            y_max=sol_attrs.y_max + layer_thick("y", "max"),
            y_min=sol_attrs.y_min + layer_thick("y", "min"),
            z_max=sol_attrs.z_max + layer_thick("z", "max"),
            z_min=sol_attrs.z_min + layer_thick("z", "min"),
        )

        for source in sources:
            for k, v in simu_region.items():
                direction, minmax = k.split("_")

                if minmax == "min":
                    if k in source:
                        if round(source[k], 10) <= round(v, 10):
                            warn_print(
                                f"{source.name} in PML layer, need fit {k} > {v}, get {source[k]}"
                            )

                    if direction in source:
                        if round(source[k]) <= round(v, 10):
                            warn_print(
                                f"{source.name} in PML layer, need fit {direction} > {v}, get "
                                f"{source[direction]}"
                            )

                if minmax == "max":
                    if k in source:
                        if round(source[k], 10) >= round(v, 10):
                            warn_print(
                                f"{source.name} need fit {k} < {v}, get {source[k]}"
                            )
                    if direction in source:
                        if round(source[direction], 10) >= round(v, 10):
                            warn_print(
                                f"{source.name} need fit {k} < {v}, get {source[direction]}"
                            )


def __project_check_port(project: MosProject, task_type):
    from maxoptics.var.models import FDE
    from maxoptics.var.models import EME
    from maxoptics.var.models import FDTD

    solver = project.solver
    if isinstance(solver, FDE):
        pass

    elif isinstance(solver, EME):

        def check_eme_port():
            ports: List[EmePort] = []
            for name, port in yield_components_with_class(EmePort, project):
                ports.append(port)

            assert len(ports) >= 2, "EME need at least 2 ports"
            locations = [_.attrs.port_location for _ in ports]
            assert len(set(locations)), "EME need ports at both side"

        if task_type != Simu_Index_Monitor:
            check_eme_port()

    elif isinstance(solver, FDTD):

        def check_fdtd_port():
            ports: List[FDTDPort] = []
            for name, port in yield_components_with_class(FDTDPort, project):
                ports.append(port)

            assert len(ports) >= 1, "FDTD need at least 1 source port"

        if project.port_groups:
            check_fdtd_port()

    else:
        raise ValueError("Unknown Solver type {}".format(solver))


# %%
