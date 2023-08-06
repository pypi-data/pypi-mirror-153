# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("Region",)


class Region(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = RegionActions(component_ref)
        self.attrs = RegionAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "icon-region2"
        self.id = ""
        self.locked = False
        self.name = "Region"
        self.order = "0"
        self.tabs = ["General", "Geometry"]
        self.type = RegionType(component_ref)
        self.__belong2__ = {"active": ["Document"]}
        super().__init__(project_ref)


class RegionActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addRegion = "addRegion"

        super().__init__(component_ref)


class RegionAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.bg_material = "none"
        self.dimension = 0
        self.rotate_x = 0
        self.rotate_y = 0
        self.rotate_z = 0
        self.spatial = RegionAttrsSpatial(component_ref)
        self.wireframe = True
        self.x = 0.1
        self.x_max = 0
        self.x_min = 0
        self.x_span = 0
        self.xmaxbc = 1
        self.xmaxshell = 0
        self.xminbc = 1
        self.xminshell = 0
        self.y = 0
        self.y_max = 0
        self.y_min = 0
        self.y_span = 8
        self.ymaxbc = 1
        self.ymaxshell = 0
        self.yminbc = 1
        self.yminshell = 0
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 8
        self.zmaxbc = 1
        self.zmaxshell = 0
        self.zminbc = 1
        self.zminshell = 0

        super().__init__(component_ref)


class RegionAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RegionType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RegionTypeActions(component_ref)
        self.attrs = RegionTypeAttrs(component_ref)
        self.base = RegionTypeBase(component_ref)
        self.icon = "icon-region2"
        self.name = "Region"
        self.order = "0"
        self.tabs = ["General", "Geometry"]

        super().__init__(component_ref)


class RegionTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addRegion = "addRegion"

        super().__init__(component_ref)


class RegionTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.bg_material = "none"
        self.dimension = 0
        self.rotate_x = 0
        self.rotate_y = 0
        self.rotate_z = 0
        self.spatial = RegionTypeAttrsSpatial(component_ref)
        self.wireframe = True
        self.x = 0.1
        self.x_max = 0
        self.x_min = 0
        self.x_span = 0
        self.xmaxbc = 1
        self.xmaxshell = 0
        self.xminbc = 1
        self.xminshell = 0
        self.y = 0
        self.y_max = 0
        self.y_min = 0
        self.y_span = 8
        self.ymaxbc = 1
        self.ymaxshell = 0
        self.yminbc = 1
        self.yminshell = 0
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 8
        self.zmaxbc = 1
        self.zmaxshell = 0
        self.zminbc = 1
        self.zminshell = 0

        super().__init__(component_ref)


class RegionTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RegionTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RegionTypeBaseActions(component_ref)
        self.attrs = RegionTypeBaseAttrs(component_ref)
        self.base = RegionTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class RegionTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RegionTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = RegionTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class RegionTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RegionTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RegionTypeBaseBaseActions(component_ref)
        self.attrs = RegionTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class RegionTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class RegionTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
