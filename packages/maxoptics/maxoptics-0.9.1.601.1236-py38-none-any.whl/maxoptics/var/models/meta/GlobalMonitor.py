# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("GlobalMonitor",)


class GlobalMonitor(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = GlobalMonitorActions(component_ref)
        self.attrs = GlobalMonitorAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "icona-globaloption"
        self.id = ""
        self.locked = False
        self.name = "GlobalMonitor"
        self.order = 0
        self.order = "0"
        self.tabs = ["Frequency Power", "Advanced"]
        self.type = GlobalMonitorType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class GlobalMonitorActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class GlobalMonitorAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actual_sampling = 2694.53
        self.desired_sampling = 1498.96
        self.down_sample_time = 17
        self.frequency_center = 193.414
        self.frequency_max = 199.862
        self.frequency_min = 187.37
        self.frequency_points = 5
        self.frequency_span = 12.492
        self.min_sampling_per_cycle = 2
        self.nyquist_limit = 2662.59
        self.sample_spacing = 0
        self.spacing_limit = 0
        self.spacing_type = 0
        self.spatial = GlobalMonitorAttrsSpatial(component_ref)
        self.use_source_limits = 0
        self.use_wavelength_spacing = 1
        self.wavelength_center = 1.55
        self.wavelength_max = 1.6
        self.wavelength_min = 1.5
        self.wavelength_span = 0.1

        super().__init__(component_ref)


class GlobalMonitorAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class GlobalMonitorType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = GlobalMonitorTypeActions(component_ref)
        self.attrs = GlobalMonitorTypeAttrs(component_ref)
        self.base = GlobalMonitorTypeBase(component_ref)
        self.icon = "icona-globaloption"
        self.name = "GlobalMonitor"
        self.order = "0"
        self.tabs = ["Frequency Power", "Advanced"]

        super().__init__(component_ref)


class GlobalMonitorTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class GlobalMonitorTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actual_sampling = 2694.53
        self.desired_sampling = 1498.96
        self.down_sample_time = 17
        self.frequency_center = 193.414
        self.frequency_max = 199.862
        self.frequency_min = 187.37
        self.frequency_points = 5
        self.frequency_span = 12.492
        self.min_sampling_per_cycle = 2
        self.nyquist_limit = 2662.59
        self.sample_spacing = 0
        self.spacing_limit = 0
        self.spacing_type = 0
        self.spatial = GlobalMonitorTypeAttrsSpatial(component_ref)
        self.use_source_limits = 0
        self.use_wavelength_spacing = 1
        self.wavelength_center = 1.55
        self.wavelength_max = 1.6
        self.wavelength_min = 1.5
        self.wavelength_span = 0.1

        super().__init__(component_ref)


class GlobalMonitorTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class GlobalMonitorTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = GlobalMonitorTypeBaseActions(component_ref)
        self.attrs = GlobalMonitorTypeBaseAttrs(component_ref)
        self.base = GlobalMonitorTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class GlobalMonitorTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class GlobalMonitorTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = GlobalMonitorTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class GlobalMonitorTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class GlobalMonitorTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = GlobalMonitorTypeBaseBaseActions(component_ref)
        self.attrs = GlobalMonitorTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class GlobalMonitorTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class GlobalMonitorTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
