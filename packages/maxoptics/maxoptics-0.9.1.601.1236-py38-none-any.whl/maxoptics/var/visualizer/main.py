from .v0_3 import (
    V03EMEResultHandler,
    V03ModeExpansionResultHandler,
    V03PDResultHandler,
    V03ModulatorResultHandler,
    V03UserImport,
)
from .v0_4 import (
    V04FDEResultHandler,
    V04FDESweepResultHandler,
    V04EMEResultHandler,
    V04EMESweepResultHandler,
    V04FDTDResultHandler,
    V04FDTDSweepResultHandler,
    V04FDTDSmatrixResultHandler,
    V04FDTDIndexResultHandler,
    V04ModeExpansionResultHandler,
    V04EMEParameterSweepResultHandler,
)


class ReMeshResultHandler:
    ...


class FDEResultHandler(V04FDEResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "FDE"


class FDESweepResultHandler(V04FDESweepResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "FDE_SWEEP"


class EMEResultHandler(V03EMEResultHandler, V04EMEResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "EME_EME"


class EMESweepResultHandler(V04EMESweepResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "EME_SWEEP"


class EMEParameterSweepResultHandler(V04EMEParameterSweepResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "EME_SWEEP_PARAMS"


class FDTDResultHandler(V04FDTDResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "FDTD"


class FDTDSweepResultHandler(V04FDTDSweepResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "FDTD_SWEEP"


class FDTDSmatrixResultHandler(V04FDTDSmatrixResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "FDTD_SMATRIX"


class FDTDIndexResultHandler(V04FDTDIndexResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "INDEX_MONITOR"


class ModeExpansionResultHandler(
    V03ModeExpansionResultHandler, V04ModeExpansionResultHandler
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "MODE_EXPANSION"


class PDResultHandler(V03PDResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "PD"


class ModulatorResultHandler(V03ModulatorResultHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = "SIMODULATOR"


class UserImport(V03UserImport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = ""
