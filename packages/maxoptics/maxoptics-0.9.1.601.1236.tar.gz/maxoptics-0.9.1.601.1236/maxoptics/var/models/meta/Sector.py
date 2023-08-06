# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("Sector",)


class Sector(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = SectorActions(component_ref)
        self.attrs = SectorAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconsector"
        self.id = ""
        self.locked = False
        self.name = "Sector"
        self.order = 6
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = SectorType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class SectorActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SectorAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.angle = 45
        self.expre_angle = ""
        self.expre_radius = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = SectorAttrsExtrude(component_ref)
        self.index_union = SectorAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.radius = 5
        self.rotate_z = 0
        self.spatial = SectorAttrsSpatial(component_ref)
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


class SectorAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class SectorAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class SectorAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SectorType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SectorTypeActions(component_ref)
        self.attrs = SectorTypeAttrs(component_ref)
        self.base = SectorTypeBase(component_ref)
        self.icon = "iconsector"
        self.name = "Sector"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class SectorTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SectorTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.angle = 45
        self.expre_angle = ""
        self.expre_radius = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = SectorTypeAttrsExtrude(component_ref)
        self.index_union = SectorTypeAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.radius = 5
        self.rotate_z = 0
        self.spatial = SectorTypeAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class SectorTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class SectorTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class SectorTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SectorTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SectorTypeBaseActions(component_ref)
        self.attrs = SectorTypeBaseAttrs(component_ref)
        self.base = SectorTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class SectorTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SectorTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = SectorTypeBaseAttrsExtrude(component_ref)
        self.index_union = SectorTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = SectorTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class SectorTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class SectorTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class SectorTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SectorTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SectorTypeBaseBaseActions(component_ref)
        self.attrs = SectorTypeBaseBaseAttrs(component_ref)
        self.base = SectorTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class SectorTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SectorTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = SectorTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class SectorTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class SectorTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SectorTypeBaseBaseBaseActions(component_ref)
        self.attrs = SectorTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class SectorTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class SectorTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
