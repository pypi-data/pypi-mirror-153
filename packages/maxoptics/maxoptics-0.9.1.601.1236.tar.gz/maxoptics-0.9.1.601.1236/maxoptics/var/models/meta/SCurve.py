# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("SCurve",)


class SCurve(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = SCurveActions(component_ref)
        self.attrs = SCurveAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconcurve1"
        self.id = ""
        self.locked = False
        self.name = "SCurve"
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = SCurveType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class SCurveActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SCurveAttrs(ProjectComponentAttrsBase):
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
        self.extrude = SCurveAttrsExtrude(component_ref)
        self.index_union = SCurveAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = SCurveAttrsSpatial(component_ref)
        self.w = 0.5
        self.x = 0
        self.x0 = 0
        self.x1 = 1.5
        self.x2 = 3.5
        self.x3 = 5
        self.y = 0
        self.y0 = 0
        self.y1 = 0
        self.y2 = 2
        self.y3 = 2
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class SCurveAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class SCurveAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class SCurveAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SCurveType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SCurveTypeActions(component_ref)
        self.attrs = SCurveTypeAttrs(component_ref)
        self.base = SCurveTypeBase(component_ref)
        self.icon = "iconcurve1"
        self.name = "SCurve"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class SCurveTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SCurveTypeAttrs(ProjectComponentAttrsBase):
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
        self.extrude = SCurveTypeAttrsExtrude(component_ref)
        self.index_union = SCurveTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = SCurveTypeAttrsSpatial(component_ref)
        self.w = 0.5
        self.x = 0
        self.x0 = 0
        self.x1 = 1.5
        self.x2 = 3.5
        self.x3 = 5
        self.y = 0
        self.y0 = 0
        self.y1 = 0
        self.y2 = 2
        self.y3 = 2
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class SCurveTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class SCurveTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class SCurveTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SCurveTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SCurveTypeBaseActions(component_ref)
        self.attrs = SCurveTypeBaseAttrs(component_ref)
        self.base = SCurveTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class SCurveTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SCurveTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = SCurveTypeBaseAttrsExtrude(component_ref)
        self.index_union = SCurveTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = SCurveTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class SCurveTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class SCurveTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class SCurveTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SCurveTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SCurveTypeBaseBaseActions(component_ref)
        self.attrs = SCurveTypeBaseBaseAttrs(component_ref)
        self.base = SCurveTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class SCurveTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SCurveTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = SCurveTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class SCurveTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SCurveTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SCurveTypeBaseBaseBaseActions(component_ref)
        self.attrs = SCurveTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class SCurveTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class SCurveTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
