# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Monitor
from weakref import ref

__all__ = ("IndexMonitor",)


class IndexMonitor(Monitor):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = IndexMonitorActions(component_ref)
        self.attrs = IndexMonitorAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconMonitor2"
        self.id = ""
        self.locked = False
        self.name = "IndexMonitor"
        self.order = 1
        self.order = "0"
        self.tabs = ["General", "Geometry"]
        self.type = IndexMonitorType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class IndexMonitorActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class IndexMonitorAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
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
        self.monitor_setting = IndexMonitorAttrsMonitor_setting(component_ref)
        self.monitor_type = 5
        self.override_global_options = 0
        self.simulation_type = 0
        self.spatial = IndexMonitorAttrsSpatial(component_ref)
        self.use_relative_coordinates = 1
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


class IndexMonitorAttrsMonitor_setting(ProjectComponentAttrsBase):
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


class IndexMonitorAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class IndexMonitorType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = IndexMonitorTypeActions(component_ref)
        self.attrs = IndexMonitorTypeAttrs(component_ref)
        self.base = IndexMonitorTypeBase(component_ref)
        self.icon = "iconMonitor2"
        self.name = "IndexMonitor"
        self.order = "0"
        self.tabs = ["General", "Geometry"]

        super().__init__(component_ref)


class IndexMonitorTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class IndexMonitorTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.down_sample_x = 1
        self.down_sample_y = 1
        self.down_sample_z = 1
        self.monitor_setting = IndexMonitorTypeAttrsMonitor_setting(
            component_ref
        )
        self.monitor_type = 5
        self.override_global_options = 0
        self.simulation_type = 0
        self.spatial = IndexMonitorTypeAttrsSpatial(component_ref)
        self.use_relative_coordinates = 1
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


class IndexMonitorTypeAttrsMonitor_setting(ProjectComponentAttrsBase):
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


class IndexMonitorTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class IndexMonitorTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = IndexMonitorTypeBaseActions(component_ref)
        self.attrs = IndexMonitorTypeBaseAttrs(component_ref)
        self.base = IndexMonitorTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class IndexMonitorTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class IndexMonitorTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = IndexMonitorTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class IndexMonitorTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class IndexMonitorTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = IndexMonitorTypeBaseBaseActions(component_ref)
        self.attrs = IndexMonitorTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class IndexMonitorTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class IndexMonitorTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
