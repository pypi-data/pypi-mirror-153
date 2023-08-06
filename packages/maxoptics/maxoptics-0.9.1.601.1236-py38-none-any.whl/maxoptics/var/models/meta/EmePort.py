# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Port
from weakref import ref

__all__ = ("EmePort",)


class EmePort(Port):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = EmePortActions(component_ref)
        self.attrs = EmePortAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconPort"
        self.id = ""
        self.locked = False
        self.name = "ep0"
        self.order = 2
        self.order = "0"
        self.tabs = ["Geometry", "EME Port"]
        self.type = EmePortType(component_ref)
        self.__belong2__ = {"passive": ["EME"]}
        super().__init__(project_ref)


class EmePortActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EmePortAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.amp = "amplitude"
        self.auto_update = 0
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.component = "Ex"
        self.currentFile = ""
        self.details_dispersion_caiculation = 0
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
        self.file = ""
        self.frequency = 193.414
        self.frequency_plot = 1
        self.frequency_scale = 0
        self.horizontal = 0
        self.isCoverage = True
        self.modeFileName = ""
        self.mode_index = 1
        self.mode_plot = 0
        self.mode_selection = 0
        self.modeindex = 1
        self.n = 1
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.offset = 0
        self.phi = 0
        self.plot = 0
        self.plot_with = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.port_location = 0
        self.scale = False
        self.search = 0
        self.spatial = EmePortAttrsSpatial(component_ref)
        self.start_frequency = 193.414
        self.start_wavelength = 1.55
        self.stop_frequency = 200
        self.stop_wavelength = 1.49896
        self.task_id = 0
        self.theta = 0
        self.use_full_simulation_span = 0
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


class EmePortAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EmePortType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EmePortTypeActions(component_ref)
        self.attrs = EmePortTypeAttrs(component_ref)
        self.base = EmePortTypeBase(component_ref)
        self.icon = "iconPort"
        self.name = "EmePort"
        self.order = "0"
        self.tabs = ["Geometry", "EME Port"]

        super().__init__(component_ref)


class EmePortTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EmePortTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.amp = "amplitude"
        self.auto_update = 0
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.component = "Ex"
        self.currentFile = ""
        self.details_dispersion_caiculation = 0
        self.effective_index = 1
        self.frequency = 193.414
        self.frequency_plot = 1
        self.frequency_scale = 0
        self.horizontal = 0
        self.modeFileName = ""
        self.mode_index = 1
        self.mode_plot = 0
        self.mode_selection = 0
        self.n = 1
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.offset = 0
        self.phi = 0
        self.plot = 0
        self.plot_with = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.port_location = 0
        self.scale = False
        self.search = 0
        self.spatial = EmePortTypeAttrsSpatial(component_ref)
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


class EmePortTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EmePortTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EmePortTypeBaseActions(component_ref)
        self.attrs = EmePortTypeBaseAttrs(component_ref)
        self.base = EmePortTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "FdeBase"
        self.order = "0"
        self.tabs = ["Modal analysis", "Boundary conditions"]

        super().__init__(component_ref)


class EmePortTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EmePortTypeBaseAttrs(ProjectComponentAttrsBase):
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
        self.spatial = EmePortTypeBaseAttrsSpatial(component_ref)
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x_max_bc = 1
        self.x_min_bc = 1
        self.y_max_bc = 1
        self.y_min_bc = 1
        self.z_max_bc = 1
        self.z_min_bc = 1

        super().__init__(component_ref)


class EmePortTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EmePortTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EmePortTypeBaseBaseActions(component_ref)
        self.attrs = EmePortTypeBaseBaseAttrs(component_ref)
        self.base = EmePortTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class EmePortTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EmePortTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = EmePortTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class EmePortTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EmePortTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EmePortTypeBaseBaseBaseActions(component_ref)
        self.attrs = EmePortTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class EmePortTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class EmePortTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
