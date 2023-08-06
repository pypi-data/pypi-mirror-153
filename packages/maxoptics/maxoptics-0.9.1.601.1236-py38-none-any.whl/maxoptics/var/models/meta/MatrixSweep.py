# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import SweepBase
from weakref import ref

__all__ = ("MatrixSweep",)


class MatrixSweep(SweepBase):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = MatrixSweepActions(component_ref)
        self.attrs = MatrixSweepAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconPointSource"
        self.id = ""
        self.locked = False
        self.name = "MatrixSweep"
        self.parent = None
        self.order = "0"
        self.tabs = ["S-Matrix setup"]
        self.type = MatrixSweepType(component_ref)
        self.__belong2__ = {"passive": ["$<----sweep*"]}
        super().__init__(project_ref)


class MatrixSweepActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class MatrixSweepAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.Active = [0]
        self.calculate_group_delay = 0
        self.modalTitle = "Edit S-Parameter Matrix Sweep"
        self.tableData = []

        super().__init__(component_ref)


class MatrixSweepType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = MatrixSweepTypeActions(component_ref)
        self.attrs = MatrixSweepTypeAttrs(component_ref)
        self.base = MatrixSweepTypeBase(component_ref)
        self.icon = "iconPointSource"
        self.name = "MatrixSweep"
        self.order = "0"
        self.tabs = ["S-Matrix setup"]

        super().__init__(component_ref)


class MatrixSweepTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class MatrixSweepTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.modalTitle = "Edit S-Parameter Matrix Sweep"

        super().__init__(component_ref)


class MatrixSweepTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = MatrixSweepTypeBaseActions(component_ref)
        self.attrs = MatrixSweepTypeBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "Object"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class MatrixSweepTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.addNewGroup = "containerGroup"
        self.copy = "copy"
        self.disable = "disable"
        self.edit = "edit"
        self.paste = "paste"
        self.remove = "remove"
        self.rename = "rename"

        super().__init__(component_ref)


class MatrixSweepTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)
