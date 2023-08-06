"""The common module provides method for some commonly used processings."""
from typing import Any, Dict

from maxoptics.core.logger import warn_print


def standard_option(local_vars: Dict[str, Any]) -> Dict[str, Any]:
    """Return the standard output for visualizer method of option type.
    Like: {"target": "intensity","pub": {"taskId": 12345, "monitorIndex": 0}}

    Args:
        local_vars (Dict[str, Any]): `locals()` of previous method.

    Returns:
        Dict[str, Any]: Standard output.
    """
    Index = getattr(local_vars["self"], "Index")
    task_id = getattr(local_vars["self"], "task_id")

    target = local_vars["target"]

    if "monitor" in local_vars:
        pub = {
            "taskId": task_id,
            "monitorIndex": Index(local_vars["monitor"]),
        }
    else:
        pub = {"taskId": task_id}

    return {"target": target, "pub": pub}


def standard_chart(local_vars: Dict[str, Any]) -> Dict[str, Any]:
    """Return the standard output for visualizer method of chart type. Like: {"target": "line", "pub": {"taskId":
    12345, "monitorIndex": 0, "attribute": "T", "operation": "Real"}, "option": { "x": "plotX", "y": "plotY",
    "z": "0", "mode: 0}}

    Args:
        local_vars (Dict[str, Any]): The `locals()` of previous method.

    Returns:
        Dict[str, Any]: The standard output.
    """
    Index = getattr(local_vars["self"], "Index")
    task_id = getattr(local_vars["self"], "task_id")

    target = local_vars["target"]
    kwargs = local_vars["kwargs"]

    if "monitor" in local_vars:
        pub = {
            "taskId": task_id,
            "monitorIndex": Index(local_vars["monitor"]),
        }
    else:
        pub = {"taskId": task_id}

    possible_pub = ["attribute", "operation", "log"]
    extra_pub = {p: local_vars[p] for p in local_vars if p in possible_pub}
    pub.update(**extra_pub)

    for k, v in kwargs.items():
        if not isinstance(v, (str, int)):
            warn_print(
                f"Got unexpected input {k}={v}::{type(v)}, which may cause failure."
            )

    return {
        "target": target,
        "pub": pub,
        "option": kwargs,
    }
