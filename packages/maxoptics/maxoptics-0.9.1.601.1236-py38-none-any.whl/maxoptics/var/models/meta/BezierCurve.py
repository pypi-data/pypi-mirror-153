# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("BezierCurve",)


class BezierCurve(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = BezierCurveActions(component_ref)
        self.attrs = BezierCurveAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconcurve1"
        self.id = ""
        self.locked = False
        self.name = "bzc0"
        self.order = 11
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = BezierCurveType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class BezierCurveActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class BezierCurveAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_rotate_z = ""
        self.expre_w = ""
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
        self.extrude = BezierCurveAttrsExtrude(component_ref)
        self.index_union = BezierCurveAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = BezierCurveAttrsSpatial(component_ref)
        self.w = 2
        self.x = 0
        self.x0 = 2
        self.x1 = 0
        self.x2 = 0
        self.x3 = -2
        self.x_max = None
        self.x_min = None
        self.y = 0
        self.y0 = 0
        self.y1 = 0
        self.y2 = 4
        self.y3 = 4
        self.y_max = None
        self.y_min = None
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class BezierCurveAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class BezierCurveAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class BezierCurveAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class BezierCurveType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = BezierCurveTypeActions(component_ref)
        self.attrs = BezierCurveTypeAttrs(component_ref)
        self.base = BezierCurveTypeBase(component_ref)
        self.icon = "iconcurve1"
        self.name = "BezierCurve"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class BezierCurveTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class BezierCurveTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_rotate_z = ""
        self.expre_w = ""
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
        self.extrude = BezierCurveTypeAttrsExtrude(component_ref)
        self.index_union = BezierCurveTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = BezierCurveTypeAttrsSpatial(component_ref)
        self.w = 2
        self.x = 0
        self.x0 = 2
        self.x1 = 0
        self.x2 = 0
        self.x3 = -2
        self.y = 0
        self.y0 = 0
        self.y1 = 0
        self.y2 = 4
        self.y3 = 4
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class BezierCurveTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class BezierCurveTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class BezierCurveTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class BezierCurveTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = BezierCurveTypeBaseActions(component_ref)
        self.attrs = BezierCurveTypeBaseAttrs(component_ref)
        self.base = BezierCurveTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class BezierCurveTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class BezierCurveTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = BezierCurveTypeBaseAttrsExtrude(component_ref)
        self.index_union = BezierCurveTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = BezierCurveTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class BezierCurveTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class BezierCurveTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class BezierCurveTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class BezierCurveTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = BezierCurveTypeBaseBaseActions(component_ref)
        self.attrs = BezierCurveTypeBaseBaseAttrs(component_ref)
        self.base = BezierCurveTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class BezierCurveTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class BezierCurveTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = BezierCurveTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class BezierCurveTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class BezierCurveTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = BezierCurveTypeBaseBaseBaseActions(component_ref)
        self.attrs = BezierCurveTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class BezierCurveTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class BezierCurveTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
