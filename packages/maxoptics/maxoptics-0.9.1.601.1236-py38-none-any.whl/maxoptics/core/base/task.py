import time

from attr import define, field

from maxoptics.core.abc import ExportableAttrS


@define
class TaskAbstract(ExportableAttrS):
    id: int
    name: str
    create_time: field(
        converter=lambda v: time.strptime(v, "%Y/%m/%d %H:%M:%S")
    )
    status: int
    task_type: str
    root_task: int
