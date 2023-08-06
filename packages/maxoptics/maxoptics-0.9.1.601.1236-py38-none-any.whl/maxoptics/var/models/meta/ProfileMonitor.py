# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Monitor
from weakref import ref

__all__ = ("ProfileMonitor",)


class ProfileMonitor(Monitor):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = ProfileMonitorActions(component_ref)
        self.attrs = ProfileMonitorAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconRegion1"
        self.id = ""
        self.locked = False
        self.name = "ProfileMonitor"
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = ProfileMonitorType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class ProfileMonitorActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ProfileMonitorAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_resolution = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.monitor_type = 2
        self.spatial = ProfileMonitorAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = 0
        self.x_min = 0
        self.x_resolution = 100
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


class ProfileMonitorAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ProfileMonitorType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ProfileMonitorTypeActions(component_ref)
        self.attrs = ProfileMonitorTypeAttrs(component_ref)
        self.base = ProfileMonitorTypeBase(component_ref)
        self.icon = "iconRegion1"
        self.name = "ProfileMonitor"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class ProfileMonitorTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ProfileMonitorTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_resolution = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.monitor_type = 2
        self.spatial = ProfileMonitorTypeAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = 1.5
        self.x_min = -1.5
        self.x_resolution = 100
        self.x_span = 3
        self.y = 0
        self.y_max = 1.5
        self.y_min = -1.5
        self.y_span = 3
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 0

        super().__init__(component_ref)


class ProfileMonitorTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ProfileMonitorTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ProfileMonitorTypeBaseActions(component_ref)
        self.attrs = ProfileMonitorTypeBaseAttrs(component_ref)
        self.base = ProfileMonitorTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ProfileMonitorTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ProfileMonitorTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = ProfileMonitorTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class ProfileMonitorTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ProfileMonitorTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ProfileMonitorTypeBaseBaseActions(component_ref)
        self.attrs = ProfileMonitorTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ProfileMonitorTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class ProfileMonitorTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
