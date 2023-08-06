# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Monitor
from weakref import ref

__all__ = ("TimeMonitor",)


class TimeMonitor(Monitor):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = TimeMonitorActions(component_ref)
        self.attrs = TimeMonitorAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconMonitor1"
        self.id = ""
        self.locked = False
        self.name = "TimeMonitor"
        self.order = "0"
        self.tabs = ["General", "Geometry", "Data to record", "Advanced"]
        self.type = TimeMonitorType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class TimeMonitorActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class TimeMonitorAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.down_sample_time = 0
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
        self.min_sampling_per_cycle = 10
        self.monitor_type = 1
        self.output_ex = 1
        self.output_ey = 1
        self.output_ez = 1
        self.output_hx = 1
        self.output_hy = 1
        self.output_hz = 1
        self.output_power = True
        self.output_px = True
        self.output_py = True
        self.output_pz = True
        self.override_global_options = 1
        self.plugin_material = 0
        self.record_data_in_pml = True
        self.sampling_rate = 0
        self.set_time_domain = TimeMonitorAttrsSet_time_domain(component_ref)
        self.simulation_type = 0
        self.span = TimeMonitorAttrsSpan(component_ref)
        self.spatial = TimeMonitorAttrsSpatial(component_ref)
        self.spatial_interpolation = 0
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


class TimeMonitorAttrsSet_time_domain(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.number_of_snapshots = 0
        self.start_time = 0
        self.stop_method = 0
        self.stop_time = 1000

        super().__init__(component_ref)


class TimeMonitorAttrsSpan(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.length = 3
        self.normal = 0
        self.width = 2

        super().__init__(component_ref)


class TimeMonitorAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class TimeMonitorType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = TimeMonitorTypeActions(component_ref)
        self.attrs = TimeMonitorTypeAttrs(component_ref)
        self.base = TimeMonitorTypeBase(component_ref)
        self.icon = "iconMonitor1"
        self.name = "TimeMonitor"
        self.order = "0"
        self.tabs = ["General", "Geometry", "Data to record", "Advanced"]

        super().__init__(component_ref)


class TimeMonitorTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class TimeMonitorTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.down_sample_time = 0
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
        self.min_sampling_per_cycle = 10
        self.monitor_type = 1
        self.output_ex = 1
        self.output_ey = 1
        self.output_ez = 1
        self.output_hx = 1
        self.output_hy = 1
        self.output_hz = 1
        self.output_power = True
        self.output_px = True
        self.output_py = True
        self.output_pz = True
        self.plugin_material = 0
        self.record_data_in_pml = True
        self.sampling_rate = 0
        self.set_time_domain = TimeMonitorTypeAttrsSet_time_domain(
            component_ref
        )
        self.simulation_type = 0
        self.span = TimeMonitorTypeAttrsSpan(component_ref)
        self.spatial = TimeMonitorTypeAttrsSpatial(component_ref)
        self.spatial_interpolation = 0
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


class TimeMonitorTypeAttrsSet_time_domain(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.number_of_snapshots = 0
        self.start_time = 0
        self.stop_method = 0
        self.stop_time = 1000

        super().__init__(component_ref)


class TimeMonitorTypeAttrsSpan(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.length = 3
        self.normal = 0
        self.width = 2

        super().__init__(component_ref)


class TimeMonitorTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class TimeMonitorTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = TimeMonitorTypeBaseActions(component_ref)
        self.attrs = TimeMonitorTypeBaseAttrs(component_ref)
        self.base = TimeMonitorTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class TimeMonitorTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class TimeMonitorTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = TimeMonitorTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class TimeMonitorTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class TimeMonitorTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = TimeMonitorTypeBaseBaseActions(component_ref)
        self.attrs = TimeMonitorTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class TimeMonitorTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class TimeMonitorTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
