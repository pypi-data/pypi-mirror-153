from pathlib import Path
from typing import Type, Optional, Union

from maxoptics.core.base.task import TaskAbstract
from maxoptics.core.component.base.Component import SweepBase
from maxoptics.core.error import ProjectBuildError
from maxoptics.core.logger import info_print, warn_print
from maxoptics.core.project.Project import ProjectCore
from maxoptics.core.project.ProjectBase import (
    get_component_with_class,
)
from maxoptics.macros import (
    Simu_Modulator,
    Simu_PD,
    Simu_FDTD_Mode_Expansion,
    Simu_FDE,
    Simu_Index_Monitor,
    Simu_FDE_Sweep,
    Simu_EME_FDE,
    Simu_EME_Wavelength_Sweep,
    Simu_EME_Propagation_Sweep,
    Simu_EME_Parameter_Sweep,
    Simu_FDTD,
    Simu_FDTD_Parameter_Sweep,
    Simu_FDTD_Smatrix,
    Simu_EME_EME,
    Simu_Types,
)
from maxoptics.var.models import (
    FDE,
    FDTD,
    EME,
    ModeExpansion,
    FDTDPort,
    IndexMonitor,
    MatrixSweep,
)
from maxoptics.var.models import (
    MosProjectAccessory,
)
from maxoptics.var.visualizer import (
    FDEResultHandler,
    FDTDIndexResultHandler,
    FDESweepResultHandler,
    EMEResultHandler,
    EMESweepResultHandler,
    FDTDResultHandler,
    FDTDSweepResultHandler,
    ModeExpansionResultHandler,
    FDTDSmatrixResultHandler,
    PDResultHandler,
    ModulatorResultHandler,
    EMEParameterSweepResultHandler,
)


class ProjectRuns:
    def __run(self, sig, asy, *args, **kwargs):
        if "sweep" not in sig.lower():
            self.DOCUMENT.attrs.exp_obj = {}
        return self.__parent__.create_task(
            self, sig, *args, async_flag=asy, **kwargs
        )

    def run(self, task_type, **kwargs):
        key = str(task_type).upper()
        return {
            "FDE": self.run_fde,
            "FDE_SWEEP": self.run_fde_sweep,
            "EME_FDE": self.run_eme_fde,
            "EME_EME": self.run_eme_eme,
            "EME_SWEEP_WAVELENGTH": self.run_eme_wavelength_sweep,
            "EME_SWEEP_PROPAGATION": self.run_eme_propagation_sweep,
            "EME_SWEEP_PARAMS": self.run_eme_parameter_sweep,
            "FDTD": self.run_fdtd,
            "FDTD_SWEEP": self.run_fdtd_parameter_sweep,
            "FDTD_SMATRIX": self.run_fdtd_smatrix,
            "INDEX_MONITOR": self.run_index_monitor,
            "MODE_EXPANSION": self.run_fdtd_mode_expansion,
            "PD": self.run_fdtd,
            "SIMODULATOR": self.run_modulator,
        }[key](**kwargs)

    def run_calculate_modes(self, component, **kwargs) -> FDEResultHandler:
        with info_print("Calculate Modes activating..."):
            if component.attrs.mode_selection == 3:
                asy = False
                sig = Simu_FDE

                inject_tarsrc(component, sig, self)

                params, functor = self.__run(sig, asy, **kwargs)

                ret = FDEResultHandler(*params)
                functor(whale_client=ret)

                return ret
            else:
                warn_print("mode_selection != 3, Calculate Modes is omitted")
                return FDEResultHandler(0, None, None, -1)

    def run_index_monitor(
        self, component, task_info={}, **kwargs
    ) -> FDTDIndexResultHandler:
        with info_print("Index Monitor activating..."):
            assert isinstance(component, IndexMonitor)
            asy = False
            sig = Simu_Index_Monitor

            solver = self.solver

            # # disable others # TODO:???
            # if component.disabled is True:
            #     component.disabled = False
            #
            # for _, mon in yield_components_with_class(IndexMonitor, self):
            #     if mon is not component and mon.disabled is not True:
            #         info_print(f"Disable {_}")
            #         mon.disabled = True

            inject_tarsrc(component, sig, self, solver.type.name)

            task_info = {**task_info, "indexMonitorId": component.id}

            params, functor = self.__run(
                sig, asy, task_info=task_info, **kwargs
            )

            ret = FDTDIndexResultHandler(*params)
            functor(whale_client=ret)
            return ret

    # def run_user_import(self, component, **kwargs) -> UserImport:

    def run_fde(self, component=None, **kwargs):
        with info_print("FDE activating..."):
            asy = False
            sig = Simu_FDE

            inject_tarsrc(component or FDE, sig, self)

            params, functor = self.__run(sig, asy, **kwargs)

            ret = FDEResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_fde_sweep(self, component=None, **kwargs):
        with info_print("FDE Sweep activating..."):
            asy = False
            sig = Simu_FDE_Sweep

            victim = (
                component
                if component
                else get_component_with_class(FDE, self)[1]
            )
            assert isinstance(victim, (FDE, ModeExpansion, FDTDPort))

            if component is None or component.attrs.mode_selection == 3:
                if (
                    victim.attrs.start_wavelength
                    == victim.attrs.stop_wavelength
                ):
                    raise ProjectBuildError(
                        victim.name,
                        f"Got unexpected value, "
                        f"{victim.name}.attrs.start_wavelength == "
                        f"{victim.name}.attrs.stop_wavelength == {victim.attrs.start_wavelength}",
                    )
                if victim.attrs.number_of_points == 0:
                    raise ProjectBuildError(
                        victim.name,
                        f"Got unexpected value, {victim.name}.attrs.number_of_wavelength_points == 0",
                    )

                if component:
                    inject_tarsrc(component, sig, self)
                else:
                    inject_tarsrc(FDE, sig, self)
                    inject_tar_sweep(FDE, FDE, sig, self)

                params, functor = self.__run(sig, asy, **kwargs)

                ret = FDESweepResultHandler(*params)
                functor(whale_client=ret)
            else:
                warn_print("mode_selection != 3, Calculate Modes is omitted")
                return FDESweepResultHandler(0, None, None, -1)
            return ret

    def run_eme_fde(self, component=None, **kwargs):
        with info_print("EME FDE activating..."):
            asy = True
            sig = Simu_EME_FDE

            inject_tarsrc(component or EME, sig, self)

            params, functor = self.__run(sig, asy, **kwargs)

            ret = FDEResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_eme_eme(self, dep_task, component=None, **kwargs):
        with info_print("EME EME activating..."):
            asy = True
            sig = Simu_EME_EME

            inject_tarsrc(component or EME, sig, self)

            params, functor = self.__run(sig, asy, dep_task=dep_task, **kwargs)

            ret = EMEResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_eme_wavelength_sweep(self, dep_task, component=None, **kwargs):
        with info_print("EME Wavelength Sweep activating..."):
            # Before run
            eme: EME = self.solver
            eme.attrs.use_wavelength_sweep = 1
            eme.attrs.propagation = 0
            self.DOCUMENT.attrs.sweep_type = "wavelength"
            if eme.attrs.start_wavelength == eme.attrs.stop_wavelength:
                raise ProjectBuildError(
                    eme.name,
                    f"Got unexpected value, "
                    f"eme.attrs.start_wavelength == "
                    f"eme.attrs.stop_wavelength == {eme.attrs.start_wavelength}",
                )
            if eme.attrs.number_of_wavelength_points == 0:
                raise ProjectBuildError(
                    eme.name,
                    "Got unexpected value, eme.attrs.number_of_wavelength_points == 0",
                )

            asy = True
            sig = Simu_EME_Wavelength_Sweep

            inject_tarsrc(component or EME, sig, self)
            inject_tar_sweep(EME, EME, sig, self)

            params, functor = self.__run(sig, asy, dep_task=dep_task, **kwargs)

            ret = EMESweepResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_eme_propagation_sweep(self, dep_task, component=None, **kwargs):
        with info_print("EME Propagation Sweep activating..."):
            # Before run
            eme: EME = self.solver
            eme.attrs.use_wavelength_sweep = 0
            eme.attrs.propagation = 1
            self.DOCUMENT.attrs.sweep_type = "propagation"
            if eme.attrs.start == eme.attrs.stop:
                raise ProjectBuildError(
                    eme.name,
                    "Got unexpected value, eme.attrs.start == eme.attrs.stop",
                )
            if eme.attrs.number_of_points == 0:
                raise ProjectBuildError(
                    eme.name,
                    "Got unexpected value, eme.attrs.number_of_points == 0",
                )

            asy = True
            sig = Simu_EME_Propagation_Sweep

            inject_tarsrc(component or EME, sig, self)
            inject_tar_sweep(EME, EME, sig, self)

            params, functor = self.__run(sig, asy, dep_task=dep_task, **kwargs)

            ret = EMESweepResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_eme_parameter_sweep(self, component=None, **kwargs):
        with info_print("EME Parameter Sweep activating..."):
            asy = True
            sig = Simu_EME_Parameter_Sweep

            inject_tarsrc(component or EME, sig, self)
            inject_tar_sweep(EME, SweepBase, sig, self)

            params, functor = self.__run(sig, asy, **kwargs)

            ret = EMEParameterSweepResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_fdtd(self, component=None, **kwargs):
        with info_print("FDTD activating..."):
            asy = True
            sig = Simu_FDTD

            inject_tarsrc(component or FDTD, sig, self)

            params, functor = self.__run(sig, asy, **kwargs)

            ret = FDTDResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_fdtd_parameter_sweep(self, component=None, **kwargs):
        with info_print("FDTD Parameter Sweep activating..."):
            asy = True
            sig = Simu_FDTD_Parameter_Sweep

            inject_tarsrc(component or FDTD, sig, self)
            inject_tar_sweep(FDTD, SweepBase, sig, self)

            params, functor = self.__run(sig, asy, **kwargs)

            ret = FDTDSweepResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_fdtd_smatrix(self, component=None, **kwargs):
        with info_print("FDTD Matrix Sweep activating..."):
            asy = True
            sig = Simu_FDTD_Smatrix

            _, sweep = get_component_with_class(MatrixSweep, self)
            assert sweep
            assert True in [_["isActive"] for _ in sweep.attrs.tableData]

            inject_tarsrc(component or FDTD, sig, self)
            inject_tar_sweep(FDTD, SweepBase, "fdtd smatrix", self)

            params, functor = self.__run(sig, asy, **kwargs)

            ret = FDTDSmatrixResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_fdtd_mode_expansion(
        self, component: ModeExpansion, dep_task, **kwargs
    ):
        with info_print("FDTD Mode Expansion activating..."):
            asy = True
            sig = Simu_FDTD_Mode_Expansion

            # aim_mon_id = [_["id"] for _ in component.attrs.monitors_for_expansion]
            # rescue = []
            # for _, mon in yield_components_with_class((PowerMonitor, ModeExpansion), self):
            #     if mon.id not in aim_mon_id + [component.id]:
            #         if not mon.disabled:
            #             mon.disabled = True
            #             rescue.append(mon.id)

            inject_tarsrc(component, sig, self)

            params, functor = self.__run(sig, asy, dep_task=dep_task, **kwargs)

            # for _, mon in yield_components_with_class((PowerMonitor, ModeExpansion), self):
            #     if mon.id in rescue:
            #         mon.disabled = False

            ret = ModeExpansionResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_pd(self, component=None, **kwargs):
        with info_print("PD activating..."):
            asy = False
            sig = Simu_PD

            params, functor = self.__run(sig, asy, **kwargs)

            ret = PDResultHandler(*params)
            functor(whale_client=ret)
            return ret

    def run_modulator(self, component=None, **kwargs):
        with info_print("Modulator activating..."):
            asy = False
            sig = Simu_Modulator

            params, functor = self.__run(sig, asy, **kwargs)

            ret = ModulatorResultHandler(*params)
            functor(whale_client=ret)
            return ret


class MosProject(ProjectCore, ProjectRuns, MosProjectAccessory):
    def __init__(
        self,
        parent: "MaxOptics",  # noqa
        token: str,
        name: Optional[str] = None,
        project_type: Optional[str] = None,
        log_folder: Union[str, Path, None] = None,
    ):
        super(MosProject, self).__init__(
            parent, token, name, project_type, log_folder
        )
        self.DOCUMENT = self.create_document(name="Project")
        self.global_monitor = self.create_global_monitor()

    def remote_tasks(self, task_type=None):
        if task_type is not None:
            assert (
                task_type in Simu_Types
            ), f"Unsupported task type! Must be in {Simu_Types}"

        from maxoptics.var.MosIO import MaxOptics

        client: MaxOptics = self.__parent__
        remote_tasks = client.get_tasks(self, only_completed=True)

        ret = [
            TaskAbstract(
                _["task_id"],
                _["task_name"],
                _["create_time"],
                _["status"],
                _["task_type"],
                _["root_task"],
            )
            for _ in remote_tasks
        ]

        if task_type is not None:
            ret = [_ for _ in ret if _.task_type == task_type]

        return ret

    def recalc_mesh(self, task_type):
        # self.save()
        ret = self.__parent__.post(
            url="recalc_mesh",
            **dict(
                project_id=self.id,
                task_type=task_type,
                token=self.__parent__.token,
            ),
        )
        return ret["result"]


# utils
def inject_tarsrc(
    solver_klass, sig: str, project: MosProject, parent=""
) -> MosProject:
    # if issubclass(solver_klass, Solver):
    if isinstance(solver_klass, Type):
        _, solver = get_component_with_class(solver_klass, project)
        assert solver, f"{solver_klass} must be added before you run {sig}"
    else:
        solver = solver_klass

    project.DOCUMENT.attrs.tarSrc.parent = parent
    project.DOCUMENT.attrs.tarSrc.type = solver.type.name
    project.DOCUMENT.attrs.tarSrc.id = solver.id


def inject_tar_sweep(
    solver_klass, sweep_klass, sig: str, project: MosProject
) -> MosProject:
    from maxoptics.core.component.base.Component import SweepBase

    _, solver = get_component_with_class(solver_klass, project)
    _, sweep = get_component_with_class(sweep_klass, project)
    assert (
        solver
    ), f"{solver_klass} and {sweep_klass} must be added before you run {sig}"

    # ??? EME to eme
    def panic(maybe_err):
        if isinstance(maybe_err, Exception):
            raise maybe_err
        return maybe_err

    solver_ts = solver.type.name.lower()
    sweep_id = sweep.id
    project.DOCUMENT.attrs.tarSweep = [solver_ts, sweep_id]

    if not issubclass(sweep_klass, SweepBase):
        sweepd = {"attrs": panic(sweep.attrs.export), "id": sweep.id}
        sweepd["tarSrc"] = project.DOCUMENT.attrs.tarSrc
        project.DOCUMENT.attrs.sweep.set(solver_ts, [sweepd])
