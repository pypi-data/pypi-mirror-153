# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import OtherComponent
from weakref import ref

__all__ = ("Document",)


class Document(OtherComponent):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = DocumentActions(component_ref)
        self.attrs = DocumentAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "suanfa8"
        self.id = ""
        self.locked = False
        self.name = "Document"
        self.order = 0
        self.order = "0"
        self.tabs = ["Geometry"]
        self.type = DocumentType(component_ref)
        self.__belong2__ = {"passive": ["$<----tree"]}
        super().__init__(project_ref)


class DocumentActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class DocumentAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.configGlobleParam = []
        self.configuration = DocumentAttrsConfiguration(component_ref)
        self.drawGrid = DocumentAttrsDrawGrid(component_ref)
        self.exp_obj = {}
        self.h = 50
        self.pConfig = DocumentAttrsPConfig(component_ref)
        self.sweep = DocumentAttrsSweep(component_ref)
        self.tarSrc = DocumentAttrsTarSrc(component_ref)
        self.tarSweep = []
        self.w = 50
        self.sweep_type = "propagation"

        super().__init__(component_ref)


class DocumentAttrsConfiguration(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.units = DocumentAttrsConfigurationUnits(component_ref)

        super().__init__(component_ref)


class DocumentAttrsConfigurationUnits(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.conductivity = "μS"
        self.frequency = "THz"
        self.length = "μm"
        self.loss = "dB/cm"
        self.resistivity = "Ω"
        self.time = "fs"

        super().__init__(component_ref)


class DocumentAttrsDrawGrid(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.dx = 1
        self.dy = 1

        super().__init__(component_ref)


class DocumentAttrsExp_obj(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class DocumentAttrsPConfig(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.keyName_0 = ""
        self.keyName_1 = ""
        self.value_0 = ""
        self.value_1 = ""

        super().__init__(component_ref)


class DocumentAttrsSweep(ProjectComponentAttrsBase):
    def __init__(self, component_ref):
        self.eme = []
        self.fdtd = []
        self.fde = []

        super().__init__(component_ref)


class DocumentAttrsTarSrc(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.id = ""
        self.parent = ""
        self.type = ""

        super().__init__(component_ref)


class DocumentType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = DocumentTypeActions(component_ref)
        self.attrs = DocumentTypeAttrs(component_ref)
        self.base = DocumentTypeBase(component_ref)
        self.icon = "suanfa8"
        self.name = "Document"
        self.order = "0"
        self.tabs = ["Geometry"]

        super().__init__(component_ref)


class DocumentTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class DocumentTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.configGlobleParam = [
            {
                "globleParamDes": "",
                "globleParamExp": "",
                "globleParamKey": "",
                "globleParamValue": "0",
            }
        ]
        self.drawGrid = DocumentTypeAttrsDrawGrid(component_ref)
        self.exp_obj = {}
        self.h = 50
        self.tarSrc = DocumentTypeAttrsTarSrc(component_ref)
        self.w = 50

        super().__init__(component_ref)


class DocumentTypeAttrsDrawGrid(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.dx = 1
        self.dy = 1

        super().__init__(component_ref)


class DocumentTypeAttrsExp_obj(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class DocumentTypeAttrsTarSrc(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.id = ""
        self.parent = ""
        self.type = ""

        super().__init__(component_ref)


class DocumentTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = DocumentTypeBaseActions(component_ref)
        self.attrs = DocumentTypeBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class DocumentTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class DocumentTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
