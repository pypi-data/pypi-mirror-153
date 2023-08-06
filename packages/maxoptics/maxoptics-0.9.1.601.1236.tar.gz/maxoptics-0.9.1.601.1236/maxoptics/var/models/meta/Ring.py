# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("Ring",)


class Ring(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = RingActions(component_ref)
        self.attrs = RingAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconRing"
        self.id = ""
        self.locked = False
        self.name = "Ring"
        self.order = 4
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = RingType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class RingActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RingAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_inner_radius = ""
        self.expre_outer_radius = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = RingAttrsExtrude(component_ref)
        self.index_union = RingAttrsIndex_union(component_ref)
        self.inner_radius = 4
        self.materialId = "P41"
        self.meshOrder = 1
        self.outer_radius = 6
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = RingAttrsSpatial(component_ref)
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


class RingAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class RingAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class RingAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RingType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RingTypeActions(component_ref)
        self.attrs = RingTypeAttrs(component_ref)
        self.base = RingTypeBase(component_ref)
        self.icon = "iconRing"
        self.name = "Ring"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class RingTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RingTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_inner_radius = ""
        self.expre_outer_radius = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = RingTypeAttrsExtrude(component_ref)
        self.index_union = RingTypeAttrsIndex_union(component_ref)
        self.inner_radius = 4
        self.materialId = "P41"
        self.meshOrder = 1
        self.outer_radius = 6
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = RingTypeAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class RingTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class RingTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class RingTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RingTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RingTypeBaseActions(component_ref)
        self.attrs = RingTypeBaseAttrs(component_ref)
        self.base = RingTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class RingTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RingTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = RingTypeBaseAttrsExtrude(component_ref)
        self.index_union = RingTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = RingTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class RingTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class RingTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class RingTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RingTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RingTypeBaseBaseActions(component_ref)
        self.attrs = RingTypeBaseBaseAttrs(component_ref)
        self.base = RingTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class RingTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class RingTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = RingTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class RingTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class RingTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = RingTypeBaseBaseBaseActions(component_ref)
        self.attrs = RingTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class RingTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class RingTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
