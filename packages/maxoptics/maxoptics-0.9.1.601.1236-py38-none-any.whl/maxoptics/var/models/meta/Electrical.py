# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("Electrical",)


class Electrical(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = ElectricalActions(component_ref)
        self.attrs = ElectricalAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "icon-ElectricalRepairs"
        self.id = ""
        self.locked = False
        self.name = "Electrical"
        self.order = "0"
        self.tabs = ["General", "Geomety"]
        self.type = ElectricalType(component_ref)
        self.__belong2__ = {"active": ["Document"]}
        super().__init__(project_ref)


class ElectricalActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addElectrical = "addElectrical"

        super().__init__(component_ref)


class ElectricalAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.bc_mode = 0
        self.domain = 1
        self.electrondes = 0
        self.force_ohmic = 0
        self.map_current = 0
        self.mat_id = 0
        self.materialId = "P41"
        self.outer_surface = 0
        self.region_solid = ""
        self.region_x = 0
        self.region_x_solid = 0
        self.region_xmax = 0
        self.region_xmax_solid = 0
        self.region_y = 0
        self.region_y_solid = 0
        self.region_ymax = 0
        self.region_ymax_solid = 0
        self.region_z = 0
        self.region_z_solid = 0
        self.region_zmax = 0
        self.region_zmax_solid = 0
        self.rse_radio = 0
        self.rse_unit = 0
        self.rse_value = 0
        self.rsh_radio = 0
        self.rsh_unit = 0
        self.rsh_value = 10
        self.small_signal = 0
        self.solid = "ge"
        self.spatial = ElectricalAttrsSpatial(component_ref)
        self.surface_type = 1
        self.sweep_type = 0
        self.voltage = 0
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


class ElectricalAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ElectricalType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ElectricalTypeActions(component_ref)
        self.attrs = ElectricalTypeAttrs(component_ref)
        self.base = ElectricalTypeBase(component_ref)
        self.icon = "icon-ElectricalRepairs"
        self.name = "Electrical"
        self.order = "0"
        self.tabs = ["General", "Geomety"]

        super().__init__(component_ref)


class ElectricalTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addElectrical = "addElectrical"

        super().__init__(component_ref)


class ElectricalTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.bc_mode = 0
        self.electrondes = 0
        self.force_ohmic = 0
        self.materialId = "P41"
        self.rse_radio = 0
        self.rse_unit = 0
        self.rse_value = 0
        self.rsh_radio = 0
        self.rsh_unit = 0
        self.rsh_value = 10
        self.small_signal = 0
        self.spatial = ElectricalTypeAttrsSpatial(component_ref)
        self.sweep_type = 0
        self.voltage = 0
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


class ElectricalTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ElectricalTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ElectricalTypeBaseActions(component_ref)
        self.attrs = ElectricalTypeBaseAttrs(component_ref)
        self.base = ElectricalTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ElectricalTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class ElectricalTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = ElectricalTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class ElectricalTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class ElectricalTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = ElectricalTypeBaseBaseActions(component_ref)
        self.attrs = ElectricalTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class ElectricalTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class ElectricalTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
