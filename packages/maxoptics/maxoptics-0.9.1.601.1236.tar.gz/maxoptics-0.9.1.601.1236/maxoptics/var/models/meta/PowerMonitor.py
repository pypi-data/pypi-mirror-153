# coding=utf-8
from weakref import ref

from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Monitor

__all__ = ("PowerMonitor",)


class PowerMonitor(Monitor):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = []
        self.attrs = PowerMonitorAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconMonitor1"
        self.id = ""
        self.locked = False
        self.name = "PowerMonitor"
        self.order = "0"
        self.tabs = ["General", "Geometry", "Data to record", "Advanced"]
        self.type = PowerMonitorType(component_ref)
        self.__belong2__ = {"active": ["Document"], "passive": ["Document"]}
        super().__init__(project_ref)


class PowerMonitorAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        # Special
        self.mode_expansion = {}
        self._monitor_type = 0
        self._objLink = []
        self.apodization_center = 500
        self.apodization_freq_width = 4.41271
        self.apodization_time_width = 100
        self.center = PowerMonitorAttrsCenter(component_ref)
        self.data = 10
        self.down_sample_x = 1
        self.down_sample_y = 1
        self.down_sample_z = 1
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
        self.frequency_points = 5
        self.monitor_setting = PowerMonitorAttrsMonitor_setting(component_ref)
        self.monitor_type = 5
        self.output_ex = 1
        self.output_ey = 1
        self.output_ez = 1
        self.output_hx = 1
        self.output_hy = 1
        self.output_hz = 1
        self.output_power = 1
        self.output_px = 0
        self.output_py = 0
        self.output_pz = 0
        self.override_global_monitor_settings = (
            PowerMonitorAttrsOverride_global_monitor_settings(component_ref)
        )
        self.override_global_options = 1
        self.partial_spectral_average = 0
        self.record_data_in_pml = False
        self.sample_spacing = 0
        self.simulation_type = 0
        self.span = PowerMonitorAttrsSpan(component_ref)
        self.spatial = PowerMonitorAttrsSpatial(component_ref)
        self.spatial_interpolation = 0
        self.standard_fourier_transform = 1
        self.total_spectral_average = 0
        self.use_relative_coordinates = 1
        self.use_source_limits = 0
        self.use_wavelength_spacing = 1
        self.x = 0
        self.x_max = 0
        self.x_min = 0
        self.x_span = 0
        self.y = 0
        self.y_max = 0
        self.y_min = 0
        self.y_span = 0
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 0

        super().__init__(component_ref)


class PowerMonitorAttrsCenter(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.frequency_center = 0
        self.frequency_max = 0
        self.frequency_min = 0
        self.frequency_span = 0
        self.spacing_limit = 0
        self.spacing_type = 0
        self.wavelength_center = 0
        self.wavelength_max = 0
        self.wavelength_min = 0
        self.wavelength_span = 0

        super().__init__(component_ref)


class PowerMonitorAttrsMonitor_setting(ProjectComponentAttrsBase):
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
        self.use_wavelength_spacing = 1
        self.wavelength_center = 1.55
        self.wavelength_max = 1.6
        self.wavelength_min = 1.5
        self.wavelength_span = 0.1

        super().__init__(component_ref)


class PowerMonitorAttrsOverride_global_monitor_settings(
    ProjectComponentAttrsBase
):
    def __init__(self, component_ref):
        self.actual_sampling = 0
        self.desired_sampling = 0
        self.down_sample_time = 0
        self.min_sampling_per_cycle = 2
        self.nyquist_limit = 0

        super().__init__(component_ref)


class PowerMonitorAttrsSpan(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.length = 3
        self.normal = 0
        self.width = 2

        super().__init__(component_ref)


class PowerMonitorAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class PowerMonitorType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = []
        self.attrs = PowerMonitorTypeAttrs(component_ref)
        self.base = PowerMonitorTypeBase(component_ref)
        self.icon = "iconMonitor1"
        self.name = "PowerMonitor"
        self.order = "0"
        self.tabs = ["General", "Geometry", "Data to record", "Advanced"]

        super().__init__(component_ref)


class PowerMonitorTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self._monitor_type = 0
        self.apodization_center = 500
        self.apodization_freq_width = 4.41271
        self.apodization_time_width = 100
        self.center = PowerMonitorTypeAttrsCenter(component_ref)
        self.data = 10
        self.down_sample_x = 1
        self.down_sample_y = 1
        self.down_sample_z = 1
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
        self.frequency_points = 5
        self.monitor_setting = PowerMonitorTypeAttrsMonitor_setting(
            component_ref
        )
        self.monitor_type = 5
        self.output_ex = 1
        self.output_ey = 1
        self.output_ez = 1
        self.output_hx = 1
        self.output_hy = 1
        self.output_hz = 1
        self.output_power = 1
        self.output_px = 0
        self.output_py = 0
        self.output_pz = 0
        self.override_global_monitor_settings = (
            PowerMonitorTypeAttrsOverride_global_monitor_settings(
                component_ref
            )
        )
        self.override_global_options = 0
        self.partial_spectral_average = 0
        self.record_data_in_pml = False
        self.sample_spacing = 0
        self.simulation_type = 0
        self.span = PowerMonitorTypeAttrsSpan(component_ref)
        self.spatial = PowerMonitorTypeAttrsSpatial(component_ref)
        self.spatial_interpolation = 0
        self.standard_fourier_transform = 1
        self.total_spectral_average = 0
        self.use_relative_coordinates = 1
        self.use_source_limits = 0
        self.use_wavelength_spacing = 1
        self.x = 0
        self.x_max = 0
        self.x_min = 0
        self.x_span = 0
        self.y = 0
        self.y_max = 1.5
        self.y_min = -1.5
        self.y_span = 3
        self.z = 0
        self.z_max = 1.5
        self.z_min = -1.5
        self.z_span = 3

        super().__init__(component_ref)


class PowerMonitorTypeAttrsCenter(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.frequency_center = 0
        self.frequency_max = 0
        self.frequency_min = 0
        self.frequency_span = 0
        self.spacing_limit = 0
        self.spacing_type = 0
        self.wavelength_center = 0
        self.wavelength_max = 0
        self.wavelength_min = 0
        self.wavelength_span = 0

        super().__init__(component_ref)


class PowerMonitorTypeAttrsMonitor_setting(ProjectComponentAttrsBase):
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
        self.use_wavelength_spacing = 1
        self.wavelength_center = 1.55
        self.wavelength_max = 1.6
        self.wavelength_min = 1.5
        self.wavelength_span = 0.1

        super().__init__(component_ref)


class PowerMonitorTypeAttrsOverride_global_monitor_settings(
    ProjectComponentAttrsBase
):
    def __init__(self, component_ref):
        self.actual_sampling = 0
        self.desired_sampling = 0
        self.down_sample_time = 0
        self.min_sampling_per_cycle = 2
        self.nyquist_limit = 0

        super().__init__(component_ref)


class PowerMonitorTypeAttrsSpan(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.length = 3
        self.normal = 0
        self.width = 2

        super().__init__(component_ref)


class PowerMonitorTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class PowerMonitorTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = PowerMonitorTypeBaseActions(component_ref)
        self.attrs = PowerMonitorTypeBaseAttrs(component_ref)
        self.base = PowerMonitorTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class PowerMonitorTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class PowerMonitorTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.spatial = PowerMonitorTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class PowerMonitorTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class PowerMonitorTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = PowerMonitorTypeBaseBaseActions(component_ref)
        self.attrs = PowerMonitorTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class PowerMonitorTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class PowerMonitorTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)
