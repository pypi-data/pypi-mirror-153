# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("LinearTrapezoid",)


class LinearTrapezoid(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = LinearTrapezoidActions(component_ref)
        self.attrs = LinearTrapezoidAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconLinearTrapezoid"
        self.id = ""
        self.locked = False
        self.name = "tpz0"
        self.order = 10
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = LinearTrapezoidType(component_ref)
        self.__belong2__ = {"active": ["Document"], "passive": ["Document"]}
        super().__init__(project_ref)


class LinearTrapezoidActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class LinearTrapezoidAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_x0 = ""
        self.expre_x1 = ""
        self.expre_x2 = ""
        self.expre_x3 = ""
        self.expre_y = ""
        self.expre_y0 = ""
        self.expre_y1 = ""
        self.expre_y2 = ""
        self.expre_y3 = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = LinearTrapezoidAttrsExtrude(component_ref)
        self.index_union = LinearTrapezoidAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = LinearTrapezoidAttrsSpatial(component_ref)
        self.x = 0
        self.x0 = -2
        self.x1 = -4
        self.x2 = 4
        self.x3 = 2
        self.x_max = None
        self.x_min = None
        self.y = 0
        self.y0 = 2
        self.y1 = -2
        self.y2 = -2
        self.y3 = 2
        self.y_max = None
        self.y_min = None
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class LinearTrapezoidAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class LinearTrapezoidAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class LinearTrapezoidAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class LinearTrapezoidType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = LinearTrapezoidTypeActions(component_ref)
        self.attrs = LinearTrapezoidTypeAttrs(component_ref)
        self.base = LinearTrapezoidTypeBase(component_ref)
        self.icon = "iconLinearTrapezoid"
        self.name = "LinearTrapezoid"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class LinearTrapezoidTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class LinearTrapezoidTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_x0 = ""
        self.expre_x1 = ""
        self.expre_x2 = ""
        self.expre_x3 = ""
        self.expre_y = ""
        self.expre_y0 = ""
        self.expre_y1 = ""
        self.expre_y2 = ""
        self.expre_y3 = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = LinearTrapezoidTypeAttrsExtrude(component_ref)
        self.index_union = LinearTrapezoidTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = LinearTrapezoidTypeAttrsSpatial(component_ref)
        self.x = 0
        self.x0 = -2
        self.x1 = -4
        self.x2 = 4
        self.x3 = 2
        self.y = 0
        self.y0 = 2
        self.y1 = -2
        self.y2 = -2
        self.y3 = 2
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class LinearTrapezoidTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class LinearTrapezoidTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class LinearTrapezoidTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class LinearTrapezoidTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = LinearTrapezoidTypeBaseActions(component_ref)
        self.attrs = LinearTrapezoidTypeBaseAttrs(component_ref)
        self.base = LinearTrapezoidTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = LinearTrapezoidTypeBaseAttrsExtrude(component_ref)
        self.index_union = LinearTrapezoidTypeBaseAttrsIndex_union(
            component_ref
        )
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = LinearTrapezoidTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = LinearTrapezoidTypeBaseBaseActions(component_ref)
        self.attrs = LinearTrapezoidTypeBaseBaseAttrs(component_ref)
        self.base = LinearTrapezoidTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = LinearTrapezoidTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = LinearTrapezoidTypeBaseBaseBaseActions(component_ref)
        self.attrs = LinearTrapezoidTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class LinearTrapezoidTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
