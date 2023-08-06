# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("Circle",)


class Circle(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = CircleActions(component_ref)
        self.attrs = CircleAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconCircle"
        self.id = ""
        self.locked = False
        self.name = "Circle"
        self.order = 3
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = CircleType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class CircleActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CircleAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_r = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = CircleAttrsExtrude(component_ref)
        self.index_union = CircleAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.r = 4
        self.rotate_z = 0
        self.spatial = CircleAttrsSpatial(component_ref)
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


class CircleAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class CircleAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class CircleAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CircleType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CircleTypeActions(component_ref)
        self.attrs = CircleTypeAttrs(component_ref)
        self.base = CircleTypeBase(component_ref)
        self.icon = "iconCircle"
        self.name = "Circle"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class CircleTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CircleTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_r = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = CircleTypeAttrsExtrude(component_ref)
        self.index_union = CircleTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.r = 4
        self.rotate_z = 0
        self.spatial = CircleTypeAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class CircleTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class CircleTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class CircleTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CircleTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CircleTypeBaseActions(component_ref)
        self.attrs = CircleTypeBaseAttrs(component_ref)
        self.base = CircleTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class CircleTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CircleTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = CircleTypeBaseAttrsExtrude(component_ref)
        self.index_union = CircleTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = CircleTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class CircleTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class CircleTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class CircleTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CircleTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CircleTypeBaseBaseActions(component_ref)
        self.attrs = CircleTypeBaseBaseAttrs(component_ref)
        self.base = CircleTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class CircleTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class CircleTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = CircleTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class CircleTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class CircleTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = CircleTypeBaseBaseBaseActions(component_ref)
        self.attrs = CircleTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class CircleTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class CircleTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
