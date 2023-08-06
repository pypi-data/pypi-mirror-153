# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("Mesh",)


class Mesh(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = MeshActions(component_ref)
        self.attrs = MeshAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconsimulation-mesh"
        self.id = ""
        self.locked = False
        self.name = "Mesh"
        self.order = 4
        self.order = "0"
        self.tabs = ["General", "Geometry"]
        self.type = MeshType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class MeshActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class MeshAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.dx = 0.025
        self.dy = 0.025
        self.dz = 0.025
        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.override_x_mesh = 0
        self.override_y_mesh = 0
        self.override_z_mesh = 0
        self.spatial = MeshAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = 0
        self.x_min = 0
        self.x_span = 0
        self.y = 0
        self.y_max = 0
        self.y_min = 0
        self.y_span = 0
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 0

        super().__init__(component_ref)


class MeshAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class MeshType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = MeshTypeActions(component_ref)
        self.attrs = MeshTypeAttrs(component_ref)
        self.base = MeshTypeBase(component_ref)
        self.icon = "iconsimulation-mesh"
        self.name = "Mesh"
        self.order = "0"
        self.tabs = ["General", "Geometry"]

        super().__init__(component_ref)


class MeshTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class MeshTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.dx = 0.025
        self.dy = 0.025
        self.dz = 0.025
        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.override_x_mesh = 0
        self.override_y_mesh = 0
        self.override_z_mesh = 0
        self.spatial = MeshTypeAttrsSpatial(component_ref)
        self.x = 0
        self.x_max = 0
        self.x_min = 0
        self.x_span = 0
        self.y = 0
        self.y_max = 0
        self.y_min = 0
        self.y_span = 0
        self.z = 0
        self.z_max = 0
        self.z_min = 0
        self.z_span = 0

        super().__init__(component_ref)


class MeshTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class MeshTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = MeshTypeBaseActions(component_ref)
        self.attrs = MeshTypeBaseAttrs(component_ref)
        self.base = MeshTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class MeshTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class MeshTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = MeshTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class MeshTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class MeshTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = MeshTypeBaseBaseActions(component_ref)
        self.attrs = MeshTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class MeshTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class MeshTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
