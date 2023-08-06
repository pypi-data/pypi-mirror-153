# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("CustomPolygon",)


class CustomPolygon(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = CustomPolygonActions(component_ref)
        self.attrs = CustomPolygonAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconCustomPolygon"
        self.id = ""
        self.locked = False
        self.name = "CustomPolygon"
        self.order = 5
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = CustomPolygonType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class CustomPolygonActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CustomPolygonAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_rotate_z = ""
        self.expre_sides = ""
        self.expre_size = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = CustomPolygonAttrsExtrude(component_ref)
        self.index_union = CustomPolygonAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.sides = 6
        self.size = 2
        self.spatial = CustomPolygonAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = None
        self.x_min = None
        self.y = 0
        self.y_max = None
        self.y_min = None
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class CustomPolygonAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class CustomPolygonAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class CustomPolygonAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CustomPolygonType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CustomPolygonTypeActions(component_ref)
        self.attrs = CustomPolygonTypeAttrs(component_ref)
        self.base = CustomPolygonTypeBase(component_ref)
        self.icon = "iconCustomPolygon"
        self.name = "CustomPolygon"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class CustomPolygonTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CustomPolygonTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_rotate_z = ""
        self.expre_sides = ""
        self.expre_size = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = CustomPolygonTypeAttrsExtrude(component_ref)
        self.index_union = CustomPolygonTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.sides = 6
        self.size = 2
        self.spatial = CustomPolygonTypeAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class CustomPolygonTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class CustomPolygonTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class CustomPolygonTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CustomPolygonTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CustomPolygonTypeBaseActions(component_ref)
        self.attrs = CustomPolygonTypeBaseAttrs(component_ref)
        self.base = CustomPolygonTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class CustomPolygonTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CustomPolygonTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = CustomPolygonTypeBaseAttrsExtrude(component_ref)
        self.index_union = CustomPolygonTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = CustomPolygonTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class CustomPolygonTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class CustomPolygonTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class CustomPolygonTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CustomPolygonTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CustomPolygonTypeBaseBaseActions(component_ref)
        self.attrs = CustomPolygonTypeBaseBaseAttrs(component_ref)
        self.base = CustomPolygonTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class CustomPolygonTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CustomPolygonTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = CustomPolygonTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class CustomPolygonTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CustomPolygonTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CustomPolygonTypeBaseBaseBaseActions(component_ref)
        self.attrs = CustomPolygonTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class CustomPolygonTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class CustomPolygonTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
