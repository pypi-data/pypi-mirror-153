# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Source
from weakref import ref

__all__ = ("ModeSource",)


class ModeSource(Source):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = []
        self.attrs = ModeSourceAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconPointSource"
        self.id = ""
        self.locked = False
        self.name = "ModeSource"
        self.order = 1
        self.order = "0"
        self.tabs = ["General", "Geometry"]
        self.type = ModeSourceType(component_ref)
        self.__belong2__ = {"active": ["Document"], "passive": ["Document"]}
        super().__init__(project_ref)


class ModeSourceAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self._objLink = []
        self.advanced_options = ModeSourceAttrsAdvanced_options(component_ref)
        self.amplitude = 1
        self.bend_location = 0
        self.bend_location_x = 0
        self.bend_location_y = 0
        self.bend_location_z = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.cell_group = [{"cell_num": 5, "span": 1}]
        self.currentFile = ""
        self.direction = 0
        self.file = ModeSourceAttrsFile(component_ref)
        self.frequency = 193.414
        self.globalSettings = False
        self.injection_axis = 0
        self.isCoverage = False
        self.maximum_convolution_time_window = 1
        self.modeFileName = ""
        self.mode_index = 1
        self.mode_selection = 3
        self.n = 1
        self.number_of_field_profile_samples = 1
        self.number_of_trial_modes = 20
        self.originGeometry = ModeSourceAttrsOriginGeometry(component_ref)
        self.override = 0
        self.phase = 0
        self.phi = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.record_local_field = 0
        self.rotation_offset = 0
        self.search = 0
        self.set_fw = ModeSourceAttrsSet_fw(component_ref)
        self.set_maximum_convolution_time_window = 0
        self.set_time_domain = ModeSourceAttrsSet_time_domain(component_ref)
        self.set_type = 0
        self.signal_vs_time = []
        self.span = ModeSourceAttrsSpan(component_ref)
        self.spatial = ModeSourceAttrsSpatial(component_ref)
        self.spectrum_vs_frequency = []
        self.spectrum_vs_wavelength = []
        self.temperature = 300
        self.theta = 0
        self.use_max_index = 1
        self.use_relative_coordinates = 1
        self.waveform_id = 0
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


class ModeSourceAttrsAdvanced_options(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.eliminate_discontinuities = 0
        self.optimize_for_short_pulse = 1

        super().__init__(component_ref)


class ModeSourceAttrsFile(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeSourceAttrsOriginGeometry(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeSourceAttrsSet_fw(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.center_frequency = 0
        self.center_wavelength = 0
        self.frequency_span = 0
        self.frequency_start = 0
        self.frequency_stop = 0
        self.range_type = 0
        self.type = 0
        self.wavelength_span = 0
        self.wavelength_start = 0
        self.wavelength_stop = 0

        super().__init__(component_ref)


class ModeSourceAttrsSet_time_domain(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.bandwidth = 0
        self.frequency = 0
        self.offset = 0
        self.pulse_type = 0
        self.pulselength = 0

        super().__init__(component_ref)


class ModeSourceAttrsSpan(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.length = 3
        self.normal = 0
        self.width = 2

        super().__init__(component_ref)


class ModeSourceAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeSourceType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = []
        self.attrs = ModeSourceTypeAttrs(component_ref)
        self.base = ModeSourceTypeBase(component_ref)
        self.icon = "iconPointSource"
        self.name = "ModeSource"
        self.order = "0"
        self.tabs = ["General", "Geometry"]

        super().__init__(component_ref)


class ModeSourceTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.advanced_options = ModeSourceTypeAttrsAdvanced_options(
            component_ref
        )
        self.amplitude = 1
        self.bend_location = 0
        self.bend_location_x = 0
        self.bend_location_y = 0
        self.bend_location_z = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.cell_group = [{"cell_num": 5, "span": 1}]
        self.direction = 0
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
        self.globalSettings = False
        self.injection_axis = 0
        self.maximum_convolution_time_window = 1
        self.mode_index = 1
        self.mode_selection = 3
        self.n = 1
        self.number_of_field_profile_samples = 1
        self.number_of_trial_modes = 20
        self.override = 0
        self.phase = 0
        self.phi = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.record_local_field = 0
        self.rotation_offset = 0
        self.search = 0
        self.set_fw = ModeSourceTypeAttrsSet_fw(component_ref)
        self.set_maximum_convolution_time_window = 0
        self.set_time_domain = ModeSourceTypeAttrsSet_time_domain(
            component_ref
        )
        self.set_type = 0
        self.signal_vs_time = []
        self.span = ModeSourceTypeAttrsSpan(component_ref)
        self.spatial = ModeSourceTypeAttrsSpatial(component_ref)
        self.spectrum_vs_frequency = []
        self.spectrum_vs_wavelength = []
        self.temperature = 300
        self.theta = 0
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


class ModeSourceTypeAttrsAdvanced_options(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.eliminate_discontinuities = 0
        self.optimize_for_short_pulse = 1

        super().__init__(component_ref)


class ModeSourceTypeAttrsSet_fw(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.center_frequency = 0
        self.center_wavelength = 0
        self.frequency_span = 0
        self.frequency_start = 0
        self.frequency_stop = 0
        self.range_type = 0
        self.type = 0
        self.wavelength_span = 0
        self.wavelength_start = 0
        self.wavelength_stop = 0

        super().__init__(component_ref)


class ModeSourceTypeAttrsSet_time_domain(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.bandwidth = 0
        self.frequency = 0
        self.offset = 0
        self.pulse_type = 0
        self.pulselength = 0

        super().__init__(component_ref)


class ModeSourceTypeAttrsSpan(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.length = 3
        self.normal = 0
        self.width = 2

        super().__init__(component_ref)


class ModeSourceTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeSourceTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = ModeSourceTypeBaseActions(component_ref)
        self.attrs = ModeSourceTypeBaseAttrs(component_ref)
        self.base = ModeSourceTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "FdeBase"
        self.order = "0"
        self.tabs = ["Modal analysis", "Boundary conditions"]

        super().__init__(component_ref)


class ModeSourceTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeSourceTypeBaseAttrs(ProjectComponentAttrsBase):
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
        self.spatial = ModeSourceTypeBaseAttrsSpatial(component_ref)
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x_max_bc = 1
        self.x_min_bc = 1
        self.y_max_bc = 1
        self.y_min_bc = 1
        self.z_max_bc = 1
        self.z_min_bc = 1

        super().__init__(component_ref)


class ModeSourceTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeSourceTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = ModeSourceTypeBaseBaseActions(component_ref)
        self.attrs = ModeSourceTypeBaseBaseAttrs(component_ref)
        self.base = ModeSourceTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ModeSourceTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class ModeSourceTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.spatial = ModeSourceTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class ModeSourceTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ModeSourceTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = ModeSourceTypeBaseBaseBaseActions(component_ref)
        self.attrs = ModeSourceTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ModeSourceTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class ModeSourceTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)
