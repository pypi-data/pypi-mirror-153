# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Structure
from weakref import ref

__all__ = ("ArcWaveguide",)


class ArcWaveguide(Structure):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = ArcWaveguideActions(component_ref)
        self.attrs = ArcWaveguideAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconArcWaveguide"
        self.id = ""
        self.locked = False
        self.name = "ArcWaveguide"
        self.order = 9
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = ArcWaveguideType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class ArcWaveguideActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ArcWaveguideAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.angle = 45
        self.expre_angle = ""
        self.expre_innerRadius = ""
        self.expre_outerRadius = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = ArcWaveguideAttrsExtrude(component_ref)
        self.index_union = ArcWaveguideAttrsIndex_union(component_ref)
        self.innerRadius = 5
        self.materialId = "P41"
        self.meshOrder = 1
        self.outerRadius = 5.5
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = ArcWaveguideAttrsSpatial(component_ref)
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


class ArcWaveguideAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class ArcWaveguideAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class ArcWaveguideAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ArcWaveguideType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ArcWaveguideTypeActions(component_ref)
        self.attrs = ArcWaveguideTypeAttrs(component_ref)
        self.base = ArcWaveguideTypeBase(component_ref)
        self.icon = "iconArcWaveguide"
        self.name = "ArcWaveguide"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class ArcWaveguideTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ArcWaveguideTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.angle = 45
        self.expre_angle = ""
        self.expre_innerRadius = ""
        self.expre_outerRadius = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.extrude = ArcWaveguideTypeAttrsExtrude(component_ref)
        self.index_union = ArcWaveguideTypeAttrsIndex_union(component_ref)
        self.innerRadius = 5
        self.materialId = "P41"
        self.meshOrder = 1
        self.outerRadius = 5.5
        self.overrideMeshOrder = 0
        self.rotate_z = 0
        self.spatial = ArcWaveguideTypeAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0
        self.z = 0
        self.z_max = 0.5
        self.z_min = -0.5
        self.z_span = 1

        super().__init__(component_ref)


class ArcWaveguideTypeAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class ArcWaveguideTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class ArcWaveguideTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ArcWaveguideTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ArcWaveguideTypeBaseActions(component_ref)
        self.attrs = ArcWaveguideTypeBaseAttrs(component_ref)
        self.base = ArcWaveguideTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Polygon"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class ArcWaveguideTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ArcWaveguideTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.extrude = ArcWaveguideTypeBaseAttrsExtrude(component_ref)
        self.index_union = ArcWaveguideTypeBaseAttrsIndex_union(component_ref)
        self.materialId = "P41"
        self.meshOrder = 1
        self.overrideMeshOrder = 0
        self.spatial = ArcWaveguideTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class ArcWaveguideTypeBaseAttrsExtrude(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.h = 1

        super().__init__(component_ref)


class ArcWaveguideTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class ArcWaveguideTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ArcWaveguideTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ArcWaveguideTypeBaseBaseActions(component_ref)
        self.attrs = ArcWaveguideTypeBaseBaseAttrs(component_ref)
        self.base = ArcWaveguideTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ArcWaveguideTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ArcWaveguideTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = ArcWaveguideTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class ArcWaveguideTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ArcWaveguideTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ArcWaveguideTypeBaseBaseBaseActions(component_ref)
        self.attrs = ArcWaveguideTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ArcWaveguideTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class ArcWaveguideTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
