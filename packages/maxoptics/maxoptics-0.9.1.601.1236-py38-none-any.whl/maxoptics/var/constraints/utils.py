from typing import TypeVar, Type

from maxoptics.core.component.base.Component import ProjectComponent
from maxoptics.var.project import MosProject


def raise_error(error):
    """Raise a error in lambda.

    Args:
        error (Exception): error

    Raises:
        error
    """
    raise error


def assert_f(stmt, msg):
    """Assert an expression in lambda.

    Args:
        stmt (bool): Very likely already evaluated.
        msg (str): Message.

    Raises:
        AssertionError

    Returns:
        None
    """
    assert stmt, msg


T = TypeVar("T")


def cast(obj, _type: Type[T]) -> T:
    """Check type and set annotation."""
    assert isinstance(
        obj, _type
    ), f"{obj} is not a {_type}, therefore program aborted"
    return obj


def remit(project: MosProject, signal: str, actor: ProjectComponent, escape):
    """Trigger another project constraint in the checking process of current project constraint

    Args:
        project (MosProject): project
        signal (str): another constraint's label.
        actor (Optional[ProjectComponent]): component, or None.
        escape (): to be ignored.

    Returns:
        None
    """
    from maxoptics.core.utils.constraints import pr

    pr().emit(project, signal, actor, escape)
