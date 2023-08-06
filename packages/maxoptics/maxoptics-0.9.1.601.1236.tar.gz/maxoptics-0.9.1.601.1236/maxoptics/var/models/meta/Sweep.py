# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import SweepBase

from weakref import ref

__all__ = ("Sweep",)


class Sweep(SweepBase):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = SweepActions(component_ref)
        self.attrs = SweepAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconwave"
        self.id = ""
        self.locked = False
        self.name = "Sweep"
        self.parent = None
        self.order = "0"
        self.tabs = ["General"]
        self.type = SweepType(component_ref)
        self.__belong2__ = {"passive": ["$<----sweep*"]}
        super().__init__(project_ref)


class SweepActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SweepAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.checked = False
        self.modalTitle = "Edit Sweep Parameter"
        self.paramData = []
        self.pointsNum = "2"
        self.resultList = []
        self.type = 0
        self.solver = 1

        super().__init__(component_ref)


class SweepType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SweepTypeActions(component_ref)
        self.attrs = SweepTypeAttrs(component_ref)
        self.base = SweepTypeBase(component_ref)
        self.icon = "iconwave"
        self.name = "Sweep"
        self.order = "0"
        self.tabs = ["General"]

        super().__init__(component_ref)


class SweepTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class SweepTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.modalTitle = "Edit Sweep Parameter"

        super().__init__(component_ref)


class SweepTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = SweepTypeBaseActions(component_ref)
        self.attrs = SweepTypeBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class SweepTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class SweepTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
