# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("Triangle",)


class Triangle(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = TriangleActions(component_ref)
        self.attrs = TriangleAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconsanjiaoxing"
        self.id = ""
        self.locked = False
        self.name = "Triangle"
        self.order = 1
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = TriangleType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class TriangleActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class TriangleAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_x0 = ""
        self.expre_x1 = ""
        self.expre_x2 = ""
        self.expre_y = ""
        self.expre_y0 = ""
        self.expre_y1 = ""
        self.expre_y2 = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = TriangleAttrsExtrude(component_ref)
        self.index_union = TriangleAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = TriangleAttrsSpatial(component_ref)
        self.x = 0
        self.x0 = -2
        self.x1 = 2
        self.x2 = 0
        self.x_max = None
        self.x_min = None
        self.y = 0
        self.y0 = -2
        self.y1 = -2
        self.y2 = 2
        self.y_max = None
        self.y_min = None
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class TriangleAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class TriangleAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class TriangleAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class TriangleType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = TriangleTypeActions(component_ref)
        self.attrs = TriangleTypeAttrs(component_ref)
        self.base = TriangleTypeBase(component_ref)
        self.icon = "iconsanjiaoxing"
        self.name = "Triangle"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class TriangleTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class TriangleTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_x0 = ""
        self.expre_x1 = ""
        self.expre_x2 = ""
        self.expre_y = ""
        self.expre_y0 = ""
        self.expre_y1 = ""
        self.expre_y2 = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = TriangleTypeAttrsExtrude(component_ref)
        self.index_union = TriangleTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = TriangleTypeAttrsSpatial(component_ref)
        self.x = 0
        self.x0 = -2
        self.x1 = 2
        self.x2 = 0
        self.y = 0
        self.y0 = -2
        self.y1 = -2
        self.y2 = 2
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class TriangleTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class TriangleTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class TriangleTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class TriangleTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = TriangleTypeBaseActions(component_ref)
        self.attrs = TriangleTypeBaseAttrs(component_ref)
        self.base = TriangleTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class TriangleTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class TriangleTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = TriangleTypeBaseAttrsExtrude(component_ref)
        self.index_union = TriangleTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = TriangleTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class TriangleTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class TriangleTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class TriangleTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class TriangleTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = TriangleTypeBaseBaseActions(component_ref)
        self.attrs = TriangleTypeBaseBaseAttrs(component_ref)
        self.base = TriangleTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class TriangleTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class TriangleTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = TriangleTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class TriangleTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class TriangleTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = TriangleTypeBaseBaseBaseActions(component_ref)
        self.attrs = TriangleTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class TriangleTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class TriangleTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
