# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("Ellipse",)


class Ellipse(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = EllipseActions(component_ref)
        self.attrs = EllipseAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconEllipse2"
        self.id = ""
        self.locked = False
        self.name = "Ellipse"
        self.order = 8
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = EllipseType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class EllipseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EllipseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_xRadius = ""
        self.expre_y = ""
        self.expre_yRadius = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = EllipseAttrsExtrude(component_ref)
        self.index_union = EllipseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = EllipseAttrsSpatial(component_ref)
        self.x = 0
        self.xRadius = 3
        self.x_max = None
        self.x_min = None
        self.y = 0
        self.yRadius = 5
        self.y_max = None
        self.y_min = None
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class EllipseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class EllipseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class EllipseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EllipseType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EllipseTypeActions(component_ref)
        self.attrs = EllipseTypeAttrs(component_ref)
        self.base = EllipseTypeBase(component_ref)
        self.icon = "iconEllipse2"
        self.name = "Ellipse"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class EllipseTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EllipseTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_xRadius = ""
        self.expre_y = ""
        self.expre_yRadius = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = EllipseTypeAttrsExtrude(component_ref)
        self.index_union = EllipseTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = EllipseTypeAttrsSpatial(component_ref)
        self.x = 0
        self.xRadius = 3
        self.y = 0
        self.yRadius = 5
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class EllipseTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class EllipseTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class EllipseTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EllipseTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EllipseTypeBaseActions(component_ref)
        self.attrs = EllipseTypeBaseAttrs(component_ref)
        self.base = EllipseTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class EllipseTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EllipseTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = EllipseTypeBaseAttrsExtrude(component_ref)
        self.index_union = EllipseTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = EllipseTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class EllipseTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class EllipseTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class EllipseTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EllipseTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EllipseTypeBaseBaseActions(component_ref)
        self.attrs = EllipseTypeBaseBaseAttrs(component_ref)
        self.base = EllipseTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class EllipseTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EllipseTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = EllipseTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class EllipseTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EllipseTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EllipseTypeBaseBaseBaseActions(component_ref)
        self.attrs = EllipseTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class EllipseTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class EllipseTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
