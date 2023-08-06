from functools import lru_cache

from .ComponentScopeSyncer import Restrainer as ComponentRestrainer
from .ProjectScopeSyncer import Restrainer as ProjectRestrainer


@lru_cache(maxsize=1)
def pr() -> ProjectRestrainer:
    return ProjectRestrainer()


@lru_cache(maxsize=1)
def cr() -> ComponentRestrainer:
    return ComponentRestrainer()


__all__ = ("pr", "cr")
