"""The `constraints` module records most Parameter checks and Parameter linkages
"""
from functools import lru_cache


@lru_cache(maxsize=1)
def component_scope():
    """Constraints in component scope.
    Return is fix and cached.
    This method for lazy import (eliminate circular references)

    Returns:
        list[tuple[str, Callable]]: Constraints
    """

    from .component_scope_cdl import ret

    return ret


@lru_cache(maxsize=1)
def project_scope():
    """Constraints in project scope.
    Return is fix and cached.
    This method for lazy import (eliminate circular references)

    Returns:
        list[tuple[str|Callable]]: Constraints
    """
    from .project_scope_cdl import ret

    return ret
