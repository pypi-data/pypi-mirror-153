# coding=utf-8
from weakref import ref

from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Port

__all__ = ("FDTDPort",)


class FDTDPort(Port):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = FDTDPortActions(component_ref)
        self.attrs = FDTDPortAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconPort"
        self.id = ""
        self.locked = False
        self.name = "FDTDPort"
        self.order = "0"
        self.tabs = ["Geometry", "Modal properties"]
        self.type = FDTDPortType(component_ref)
        self.__belong2__ = {"passive": ["FDTDPortGroup"]}
        super().__init__(project_ref)


class FDTDPortActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class FDTDPortAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self._objLink = []
        self.amp = "amplitude"
        self.amplitude = 1
        self.auto_update = 0
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1000000
        self.bent_radius = 1000000
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.component = "E"
        self.currentFile = ""
        self.details_dispersion_caiculation = 0
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
        self.frequency_plot = 1
        self.frequency_scale = 0
        self.horizontal = 0
        self.injection_axis = 0
        self.isCoverage = False
        self.modeFileName = ""
        self.mode_index = 1
        self.mode_plot = 0
        self.mode_selection = 0
        self.n = 1
        self.number_of_field_profile_samples = 1
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.offset = 0
        self.override_global_options = 1
        self.phase = 0
        self.phi = 0
        self.plot = 0
        self.plot_with = 0
        self.pml_kappa = 1
        self.pml_layers = 10
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.scale = False
        self.search = 0
        self.spatial = FDTDPortAttrsSpatial(component_ref)
        self.start_frequency = 193.414
        self.start_wavelength = 1.55
        self.stop_frequency = 200
        self.stop_wavelength = 1.49896
        self.task_id = 0
        self.theta = 0
        self.use_full_simulation_span = 1
        self.use_max_index = 1
        self.use_relative_coordinates = 1
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


class FDTDPortAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDPortType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = FDTDPortTypeActions(component_ref)
        self.attrs = FDTDPortTypeAttrs(component_ref)
        self.base = FDTDPortTypeBase(component_ref)
        self.icon = "iconPort"
        self.name = "FDTDPort"
        self.order = "0"
        self.tabs = ["Geometry", "Modal properties"]

        super().__init__(component_ref)


class FDTDPortTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class FDTDPortTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.amp = "amplitude"
        self.amplitude = 1
        self.auto_update = 0
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1000000
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.component = "E"
        self.details_dispersion_caiculation = 0
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
        self.injection_axis = 0
        self.modeFileName = ""
        self.mode_index = 1
        self.mode_selection = 0
        self.n = 1
        self.number_of_field_profile_samples = 1
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.offset = 0
        self.phase = 0
        self.phi = 0
        self.scale = False
        self.search = 0
        self.spatial = FDTDPortTypeAttrsSpatial(component_ref)
        self.start_frequency = 193.414
        self.start_wavelength = 1.55
        self.stop_frequency = 200
        self.stop_wavelength = 1.49896
        self.task_id = 0
        self.theta = 0
        self.use_full_simulation_span = 1
        self.use_max_index = 1
        self.use_relative_coordinates = 1
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


class FDTDPortTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDPortTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = FDTDPortTypeBaseActions(component_ref)
        self.attrs = FDTDPortTypeBaseAttrs(component_ref)
        self.base = FDTDPortTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FDTDPortTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class FDTDPortTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.spatial = FDTDPortTypeBaseAttrsSpatial(component_ref)
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.frequency = 193.414
        self.n = 1
        self.number_of_trial_modes = 20
        self.pml_kappa = 1
        self.pml_layers = 10
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.search = 1
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x_max_bc = 1
        self.x_min_bc = 1
        self.y_max_bc = 1
        self.y_min_bc = 1
        self.z_max_bc = 1
        self.z_min_bc = 1

        super().__init__(component_ref)


class FDTDPortTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDPortTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = FDTDPortTypeBaseBaseActions(component_ref)
        self.attrs = FDTDPortTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FDTDPortTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class FDTDPortTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)
