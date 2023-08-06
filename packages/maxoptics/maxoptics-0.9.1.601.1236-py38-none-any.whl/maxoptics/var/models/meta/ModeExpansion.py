# coding=utf-8
from weakref import ref

from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Monitor

__all__ = ("ModeExpansion",)


class ModeExpansion(Monitor):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = ModeExpansionActions(component_ref)
        self.attrs = ModeExpansionAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconMonitor"
        self.id = ""
        self.locked = False
        self.name = "ModeExpansion"
        self.order = "0"
        self.tabs = []
        self.type = ModeExpansionType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class ModeExpansionActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeExpansionAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.amp = "amplitude"
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.bent_waveguide_settings = (
            ModeExpansionAttrsBent_waveguide_settings(component_ref)
        )
        self.calculate_group_index = 0
        self.component = "E"
        self.details_dispersion_calculation = True
        self.direction = 0
        self.effective_index = 1
        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.frequency = 193.414
        self.frequencyPlotResult = None
        self.modeIndex = 0
        self.modePlotsResult = None
        self.mode_index = 0
        self.mode_list = [1]
        self.mode_selection = 0
        self.monitor_setting = ModeExpansionAttrsMonitor_setting(component_ref)
        self.monitor_type = 0
        self.monitors_for_expansion = []
        self.n = 1
        self.name = ""
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.override_global_options = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.scale = False
        self.search = 0
        self.spatial = ModeExpansionAttrsSpatial(component_ref)
        self.start_frequency = 193.414
        self.start_wavelength = 1.55
        self.stop_frequency = 200
        self.stop_wavelength = 1.49896
        self.tableData = []
        self.taskId = 0
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x = 0
        self.x_max = 0
        self.x_max_bc = 1
        self.x_min = 0
        self.x_min_bc = 1
        self.x_span = 0
        self.y = 0
        self.y_max = 0
        self.y_max_bc = 1
        self.y_min = 0
        self.y_min_bc = 1
        self.y_span = 0
        self.z = 0
        self.z_max = 0
        self.z_max_bc = 1
        self.z_min = 0
        self.z_min_bc = 1
        self.z_span = 0

        super().__init__(component_ref)


class ModeExpansionAttrsBent_waveguide_settings(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1000000
        self.bent_waveguide = 0

        super().__init__(component_ref)


class ModeExpansionAttrsMonitor_setting(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actual_sampling = 2694.53
        self.desired_sampling = 1498.96
        self.down_sample_time = 17
        self.frequency_center = 193.6159624583333
        self.frequency_max = 199.86163866666664
        self.frequency_min = 187.37028625
        self.frequency_points = 5
        self.frequency_span = 12.491352416666643
        self.min_sampling_per_cycle = 2
        self.nyquist_limit = 2662.59
        self.sample_spacing = 0
        self.spacing_limit = 0
        self.spacing_type = 0
        self.use_source_limits = 0
        self.use_wavelength_spacing = 0
        self.wavelength_center = 1.55
        self.wavelength_max = 1.6
        self.wavelength_min = 1.5
        self.wavelength_span = 0.10000000000000009

        super().__init__(component_ref)


class ModeExpansionAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeExpansionType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = ModeExpansionTypeActions(component_ref)
        self.attrs = ModeExpansionTypeAttrs(component_ref)
        self.base = ModeExpansionTypeBase(component_ref)
        self.icon = "iconMonitor"
        self.name = "ModeExpansion"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ModeExpansionTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeExpansionTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.amp = "amplitude"
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.bent_waveguide_settings = (
            ModeExpansionTypeAttrsBent_waveguide_settings(component_ref)
        )
        self.calculate_group_index = 0
        self.component = "E"
        self.details_dispersion_calculation = True
        self.direction = 0
        self.effective_index = 1
        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.frequency = 193.414
        self.modeIndex = 0
        self.mode_list = [1]
        self.mode_selection = 0
        self.monitor_setting = ModeExpansionTypeAttrsMonitor_setting(
            component_ref
        )
        self.monitor_type = 0
        self.monitors_for_expansion = []
        self.n = 1
        self.name = ""
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.override_global_options = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.scale = False
        self.search = 1
        self.spatial = ModeExpansionTypeAttrsSpatial(component_ref)
        self.start_frequency = 193.414
        self.start_wavelength = 1.55
        self.stop_frequency = 200
        self.stop_wavelength = 1.49896
        self.tableData = []
        self.taskId = 0
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x = 0
        self.x_max = 0
        self.x_max_bc = 1
        self.x_min = 0
        self.x_min_bc = 1
        self.x_span = 0
        self.y = 0
        self.y_max = 1.5
        self.y_max_bc = 1
        self.y_min = -1.5
        self.y_min_bc = 1
        self.y_span = 3
        self.z = 0
        self.z_max = 1.5
        self.z_max_bc = 1
        self.z_min = -1.5
        self.z_min_bc = 1
        self.z_span = 3

        super().__init__(component_ref)


class ModeExpansionTypeAttrsBent_waveguide_settings(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1000000
        self.bent_waveguide = 0

        super().__init__(component_ref)


class ModeExpansionTypeAttrsMonitor_setting(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actual_sampling = 2694.53
        self.desired_sampling = 1498.96
        self.down_sample_time = 17
        self.frequency_center = 193.414
        self.frequency_max = 199.862
        self.frequency_min = 187.37
        self.frequency_points = 5
        self.frequency_span = 12.492
        self.min_sampling_per_cycle = 2
        self.nyquist_limit = 2662.59
        self.sample_spacing = 0
        self.spacing_limit = 0
        self.spacing_type = 0
        self.use_source_limits = 0
        self.use_wavelength_spacing = True
        self.wavelength_center = 1.55
        self.wavelength_max = 1.6
        self.wavelength_min = 1.5
        self.wavelength_span = 0.1

        super().__init__(component_ref)


class ModeExpansionTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeExpansionTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = ModeExpansionTypeBaseActions(component_ref)
        self.attrs = ModeExpansionTypeBaseAttrs(component_ref)
        self.base = ModeExpansionTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "FdeBase"
        self.order = "0"
        self.tabs = ["Modal analysis", "Boundary conditions"]

        super().__init__(component_ref)


class ModeExpansionTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeExpansionTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.frequency = 193.414
        self.n = 1
        self.number_of_trial_modes = 20
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.search = 0
        self.spatial = ModeExpansionTypeBaseAttrsSpatial(component_ref)
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x_max_bc = 1
        self.x_min_bc = 1
        self.y_max_bc = 1
        self.y_min_bc = 1
        self.z_max_bc = 1
        self.z_min_bc = 1

        super().__init__(component_ref)


class ModeExpansionTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeExpansionTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = ModeExpansionTypeBaseBaseActions(component_ref)
        self.attrs = ModeExpansionTypeBaseBaseAttrs(component_ref)
        self.base = ModeExpansionTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ModeExpansionTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeExpansionTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.spatial = ModeExpansionTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class ModeExpansionTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeExpansionTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = ModeExpansionTypeBaseBaseBaseActions(component_ref)
        self.attrs = ModeExpansionTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ModeExpansionTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class ModeExpansionTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)
