# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("Rectangle",)


class Rectangle(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = RectangleActions(component_ref)
        self.attrs = RectangleAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconfangxing1"
        self.id = ""
        self.locked = False
        self.name = "Rectangle"
        self.order = 2
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = RectangleType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class RectangleActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RectangleAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_rotate_z = ""
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
        self.extrude = RectangleAttrsExtrude(component_ref)
        self.index_union = RectangleAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = RectangleAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = 2
        self.x_min = -2
        self.x_span = 4
        self.y = 0
        self.y_max = 2
        self.y_min = -2
        self.y_span = 4
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class RectangleAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class RectangleAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class RectangleAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RectangleType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RectangleTypeActions(component_ref)
        self.attrs = RectangleTypeAttrs(component_ref)
        self.base = RectangleTypeBase(component_ref)
        self.icon = "iconfangxing1"
        self.name = "Rectangle"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class RectangleTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RectangleTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_rotate_z = ""
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
        self.extrude = RectangleTypeAttrsExtrude(component_ref)
        self.index_union = RectangleTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = RectangleTypeAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = 2
        self.x_min = -2
        self.x_span = 4
        self.y = 0
        self.y_max = 2
        self.y_min = -2
        self.y_span = 4
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class RectangleTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class RectangleTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class RectangleTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RectangleTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RectangleTypeBaseActions(component_ref)
        self.attrs = RectangleTypeBaseAttrs(component_ref)
        self.base = RectangleTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class RectangleTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RectangleTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = RectangleTypeBaseAttrsExtrude(component_ref)
        self.index_union = RectangleTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = RectangleTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class RectangleTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class RectangleTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class RectangleTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RectangleTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RectangleTypeBaseBaseActions(component_ref)
        self.attrs = RectangleTypeBaseBaseAttrs(component_ref)
        self.base = RectangleTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class RectangleTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RectangleTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = RectangleTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class RectangleTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RectangleTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RectangleTypeBaseBaseBaseActions(component_ref)
        self.attrs = RectangleTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class RectangleTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class RectangleTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
