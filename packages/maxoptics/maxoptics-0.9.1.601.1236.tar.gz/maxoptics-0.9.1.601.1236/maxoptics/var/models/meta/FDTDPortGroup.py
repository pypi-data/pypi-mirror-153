# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import PortGroup
from weakref import ref

__all__ = ("FDTDPortGroup",)


class FDTDPortGroup(PortGroup):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = FDTDPortGroupActions(component_ref)
        self.attrs = FDTDPortGroupAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconPort"
        self.id = ""
        self.locked = False
        self.name = "FDTDPortGroup"
        self.order = "0"
        self.tabs = []
        self.type = FDTDPortGroupType(component_ref)
        self.__belong2__ = {"passive": ["Document"]}
        super().__init__(project_ref)


class FDTDPortGroupActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class FDTDPortGroupAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self._objLink = []
        self.actual_sampling = 2694.53
        self.calculate_group_delay = False
        self.desired_sampling = 1498.96
        self.down_sample_time = 17
        self.fractional_offset_for_group_delay = 0.0001
        self.frequency_center = 588.878
        self.frequency_max = 794.481
        self.frequency_min = 428.275
        self.frequency_span = 321.206
        self.min_sampling_per_cycle = 2
        self.monitor_frenquency_points = 5
        self.nyquist_limit = 2662.59
        self.source_mode = ""
        self.source_port = ""
        self.spacing_limit = 0
        self.spacing_type = 0
        self.spatial = FDTDPortGroupAttrsSpatial(component_ref)
        self.use_source_limits = 0
        self.use_wavelength_spacing = 1
        self.waveform_id = 0
        self.waveform_name = ""
        self.wavelength_center = 0.55
        self.wavelength_max = 0.7
        self.wavelength_min = 0.4
        self.wavelength_span = 0.3
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDPortGroupAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDPortGroupType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = FDTDPortGroupTypeActions(component_ref)
        self.attrs = FDTDPortGroupTypeAttrs(component_ref)
        self.base = FDTDPortGroupTypeBase(component_ref)
        self.icon = "iconPort"
        self.name = "FDTDPortGroup"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FDTDPortGroupTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class FDTDPortGroupTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actual_sampling = 2694.53
        self.calculate_group_delay = False
        self.desired_sampling = 1498.96
        self.down_sample_time = 17
        self.fractional_offset_for_group_delay = 0.0001
        self.frequency_center = 588.878
        self.frequency_max = 794.481
        self.frequency_min = 428.275
        self.frequency_span = 321.206
        self.min_sampling_per_cycle = 2
        self.monitor_frenquency_points = 5
        self.nyquist_limit = 2662.59
        self.source_mode = ""
        self.source_port = ""
        self.spacing_limit = 0
        self.spacing_type = 0
        self.spatial = FDTDPortGroupTypeAttrsSpatial(component_ref)
        self.use_source_limits = 0
        self.use_wavelength_spacing = 1
        self.waveform_id = 0
        self.waveform_name = ""
        self.wavelength_center = 0.55
        self.wavelength_max = 0.7
        self.wavelength_min = 0.4
        self.wavelength_span = 0.3

        super().__init__(component_ref)


class FDTDPortGroupTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDPortGroupTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = FDTDPortGroupTypeBaseActions(component_ref)
        self.attrs = FDTDPortGroupTypeBaseAttrs(component_ref)
        self.base = FDTDPortGroupTypeBaseBase(component_ref)
        self.icon = "suanfa8"
        self.name = "SpatialObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FDTDPortGroupTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)


class FDTDPortGroupTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.spatial = FDTDPortGroupTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class FDTDPortGroupTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDPortGroupTypeBaseBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.actions = FDTDPortGroupTypeBaseBaseActions(component_ref)
        self.attrs = FDTDPortGroupTypeBaseBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FDTDPortGroupTypeBaseBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class FDTDPortGroupTypeBaseBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        super().__init__(component_ref)
