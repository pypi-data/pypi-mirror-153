# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("Charge",)


class Charge(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = ChargeActions(component_ref)
        self.attrs = ChargeAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "icon-suanfa"
        self.id = ""
        self.locked = False
        self.name = "charge"
        self.order = "0"
        self.tabs = ["General", "Mesh", "Transient", "Advanced"]
        self.type = ChargeType(component_ref)
        self.__belong2__ = {"active": ["Document"]}
        super().__init__(project_ref)


class ChargeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addCharge = "addCharge"

        super().__init__(component_ref)


class ChargeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.background_material = "P41"
        self.convergence_criteria = 0
        self.convergence_method = 0
        self.dc_update_mode = 0
        self.dds_iteration_limit = 40
        self.dds_iteration_limit_update = 5
        self.deflection_tolerance = 0.01
        self.delta_time_step = 1000
        self.dx = 0.1
        self.dy = 0.1
        self.dz = 0.1
        self.enable_initialization = 0
        self.fermi_statistics = 0
        self.global_iteration_limit = 40
        self.gradient_mixing = 0
        self.ht_iteration_limit = 40
        self.ht_iteration_limit_update = 100
        self.light_power = 0.00065
        self.max_edge_length = 0.01
        self.max_refine_steps = 2000
        self.max_time_step = 100000
        self.mesh_type = 0
        self.min_edge_length = 0.01
        self.min_time_step = 200
        self.multithreading = 0
        self.multithreading_num = 1
        self.norm_length = 100
        self.nr_ratio = 0
        self.override = False
        self.override_deflection_tolerance = False
        self.poisson_iteration_limit = 40
        self.poisson_iteration_limit_update = 20
        self.primary_monitor = ""
        self.residual_abs_tol = 0.001
        self.result = "3,5"
        self.sensitivity = 30
        self.sensitivity_advanced = 0
        self.simulation_region = 0
        self.simulation_temperature = 300
        self.solver_mode = 0
        self.solver_type = 1
        self.temperature_dependence = 0
        self.triangle_quality = 5
        self.update_abs_tol = 0.001
        self.update_rel_tol = "1e-06"
        self.use_global = 1
        self.use_relative = 0
        self.user_defult = 1

        super().__init__(component_ref)


class ChargeType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ChargeTypeActions(component_ref)
        self.attrs = ChargeTypeAttrs(component_ref)
        self.base = ChargeTypeBase(component_ref)
        self.icon = "icon-suanfa"
        self.name = "Charge"
        self.order = "0"
        self.tabs = ["General", "Mesh", "Transient", "Advanced"]

        super().__init__(component_ref)


class ChargeTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addCharge = "addCharge"

        super().__init__(component_ref)


class ChargeTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.background_material = "P41"
        self.convergence_criteria = 0
        self.convergence_method = 0
        self.dc_update_mode = 0
        self.dds_iteration_limit = 40
        self.dds_iteration_limit_update = 5
        self.deflection_tolerance = 0.01
        self.delta_time_step = 1000
        self.dx = 0.1
        self.dy = 0.1
        self.dz = 0.1
        self.enable_initialization = 0
        self.fermi_statistics = 0
        self.global_iteration_limit = 40
        self.gradient_mixing = 0
        self.ht_iteration_limit = 40
        self.ht_iteration_limit_update = 100
        self.light_power = 0.00065
        self.max_edge_length = 0.01
        self.max_refine_steps = 2000
        self.max_time_step = 100000
        self.mesh_type = 0
        self.min_edge_length = 0.01
        self.min_time_step = 200
        self.multithreading = 0
        self.multithreading_num = 1
        self.norm_length = 100
        self.nr_ratio = 0
        self.override = False
        self.override_deflection_tolerance = False
        self.poisson_iteration_limit = 40
        self.poisson_iteration_limit_update = 20
        self.primary_monitor = ""
        self.residual_abs_tol = 0.001
        self.result = "3,5"
        self.sensitivity = 30
        self.sensitivity_advanced = 0
        self.simulation_region = 0
        self.simulation_temperature = 300
        self.solver_mode = 0
        self.solver_type = 1
        self.temperature_dependence = 0
        self.triangle_quality = 5
        self.update_abs_tol = 0.001
        self.update_rel_tol = "1e-06"
        self.use_global = 1
        self.use_relative = 0
        self.user_defult = 1

        super().__init__(component_ref)


class ChargeTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ChargeTypeBaseActions(component_ref)
        self.attrs = ChargeTypeBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ChargeTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class ChargeTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
