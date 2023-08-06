# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("Constant",)


class Constant(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = ConstantActions(component_ref)
        self.attrs = ConstantAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "icon-region"
        self.id = ""
        self.locked = False
        self.name = "geDoping"
        self.order = "0"
        self.tabs = ["General"]
        self.type = ConstantType(component_ref)
        self.__belong2__ = {"active": ["Document"]}
        super().__init__(project_ref)


class ConstantActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addConstant = "addConstant"

        super().__init__(component_ref)


class ConstantAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.concentration = 1000000000000000
        self.dopant_type = 0
        self.materialId = "P41"
        self.spatial = ConstantAttrsSpatial(component_ref)
        self.use_relative = 0
        self.userEelative = True
        self.volume_domains = 0
        self.volume_solid = ""
        self.volume_type = 1
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


class ConstantAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ConstantType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ConstantTypeActions(component_ref)
        self.attrs = ConstantTypeAttrs(component_ref)
        self.base = ConstantTypeBase(component_ref)
        self.icon = "icon-region"
        self.name = "Constant"
        self.order = "0"
        self.tabs = ["General"]

        super().__init__(component_ref)


class ConstantTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addConstant = "addConstant"

        super().__init__(component_ref)


class ConstantTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.concentration = 1000000000000000
        self.dopant_type = 0
        self.materialId = "P41"
        self.spatial = ConstantTypeAttrsSpatial(component_ref)
        self.use_relative = 0
        self.userEelative = True
        self.volume_domains = 0
        self.volume_solid = ""
        self.volume_type = 1
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


class ConstantTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ConstantTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ConstantTypeBaseActions(component_ref)
        self.attrs = ConstantTypeBaseAttrs(component_ref)
        self.base = ConstantTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ConstantTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ConstantTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = ConstantTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class ConstantTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ConstantTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ConstantTypeBaseBaseActions(component_ref)
        self.attrs = ConstantTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ConstantTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class ConstantTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
