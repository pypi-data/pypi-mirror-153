# coding=utf-8
# flake8: noqa
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("Fiber",)


class Fiber(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = FiberActions(component_ref)
        self.attrs = FiberAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconfiber"
        self.id = ""
        self.locked = False
        self.name = "Fiber"
        self.order = 7
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = FiberType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class FiberActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class FiberAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.expre_l = ""
        self.expre_r = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.index_union = FiberAttrsIndex_union(component_ref)
        self.l = 20
        self.materialId = 1
        self.meshOrder = 1
        self.r = 5
        self.rotate_z = 0
        self.spatial = FiberAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = None
        self.x_min = None
        self.y = 0
        self.y_max = None
        self.y_min = None
        self.z = 0
        self.z_max = None
        self.z_min = None

        super().__init__(component_ref)


class FiberAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class FiberAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FiberType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FiberTypeActions(component_ref)
        self.attrs = FiberTypeAttrs(component_ref)
        self.base = FiberTypeBase(component_ref)
        self.icon = "iconfiber"
        self.name = "Fiber"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class FiberTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class FiberTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.expre_l = ""
        self.expre_r = ""
        self.expre_rotate_z = ""
        self.expre_x = ""
        self.expre_y = ""
        self.index_union = FiberTypeAttrsIndex_union(component_ref)
        self.l = 20
        self.materialId = 1
        self.meshOrder = 1
        self.r = 5
        self.rotate_z = 0
        self.spatial = FiberTypeAttrsSpatial(component_ref)
        self.x = 0
        self.y = 0

        super().__init__(component_ref)


class FiberTypeAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class FiberTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FiberTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FiberTypeBaseActions(component_ref)
        self.attrs = FiberTypeBaseAttrs(component_ref)
        self.base = FiberTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Mesh3D"
        self.order = "0"
        self.tabs = ["Material"]

        super().__init__(component_ref)


class FiberTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class FiberTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index_union = FiberTypeBaseAttrsIndex_union(component_ref)
        self.materialId = 1
        self.meshOrder = 1
        self.spatial = FiberTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class FiberTypeBaseAttrsIndex_union(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.index = 1.4
        self.index_units = 1

        super().__init__(component_ref)


class FiberTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FiberTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FiberTypeBaseBaseActions(component_ref)
        self.attrs = FiberTypeBaseBaseAttrs(component_ref)
        self.base = FiberTypeBaseBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FiberTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class FiberTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = FiberTypeBaseBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class FiberTypeBaseBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FiberTypeBaseBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FiberTypeBaseBaseBaseActions(component_ref)
        self.attrs = FiberTypeBaseBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FiberTypeBaseBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class FiberTypeBaseBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
