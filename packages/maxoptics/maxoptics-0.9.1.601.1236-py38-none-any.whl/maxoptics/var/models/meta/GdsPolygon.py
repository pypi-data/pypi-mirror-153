# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("GdsPolygon",)


class GdsPolygon(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = GdsPolygonActions(component_ref)
        self.attrs = GdsPolygonAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconfangxing1"
        self.id = ""
        self.locked = False
        self.name = "GdsPolygon_1"
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = GdsPolygonType(component_ref)
        self.__belong2__ = {"active": ["Document"], "passive": ["Document"]}
        super().__init__(project_ref)


class GdsPolygonActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class GdsPolygonAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = GdsPolygonAttrsExtrude(component_ref)
        self.index_union = GdsPolygonAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.points = []
        self.rotate_z = 0
        self.spatial = GdsPolygonAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 0

        super().__init__(component_ref)


class GdsPolygonAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class GdsPolygonAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class GdsPolygonAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class GdsPolygonType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = GdsPolygonTypeActions(component_ref)
        self.attrs = GdsPolygonTypeAttrs(component_ref)
        self.base = GdsPolygonTypeBase(component_ref)
        self.icon = "iconfangxing1"
        self.name = "GdsPolygon"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class GdsPolygonTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class GdsPolygonTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = GdsPolygonTypeAttrsExtrude(component_ref)
        self.index_union = GdsPolygonTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.points = []
        self.rotate_z = 0
        self.spatial = GdsPolygonTypeAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 0

        super().__init__(component_ref)


class GdsPolygonTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class GdsPolygonTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class GdsPolygonTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class GdsPolygonTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = GdsPolygonTypeBaseActions(component_ref)
        self.attrs = GdsPolygonTypeBaseAttrs(component_ref)
        self.base = GdsPolygonTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class GdsPolygonTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class GdsPolygonTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = GdsPolygonTypeBaseAttrsExtrude(component_ref)
        self.index_union = GdsPolygonTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = GdsPolygonTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class GdsPolygonTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class GdsPolygonTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class GdsPolygonTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class GdsPolygonTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = GdsPolygonTypeBaseBaseActions(component_ref)
        self.attrs = GdsPolygonTypeBaseBaseAttrs(component_ref)
        self.base = GdsPolygonTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class GdsPolygonTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class GdsPolygonTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = GdsPolygonTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class GdsPolygonTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class GdsPolygonTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = GdsPolygonTypeBaseBaseBaseActions(component_ref)
        self.attrs = GdsPolygonTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class GdsPolygonTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class GdsPolygonTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
