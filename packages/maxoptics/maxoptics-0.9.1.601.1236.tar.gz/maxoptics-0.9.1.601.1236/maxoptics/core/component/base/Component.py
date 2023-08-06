import weakref
from typing import TypeVar

from maxoptics.core.component.base.base import (
    StyleBase,
    pre_set_attribute,
    post_set_attribute,
    one_time_check,
)
from maxoptics.core.logger import error_print, warn_print
from maxoptics.core.utils import (
    nearest_words_with_damerau_levenshtein_distance,
)
from maxoptics.macros import Macro

T = TypeVar("_T")


class ProjectComponent(StyleBase):
    """A basic class that will be inherited by all components."""

    def __init__(self, project_ref):
        """Initialize basic attributes."""
        self.children = []
        self.locked = False
        self.disabled = False
        self.id = ""
        self.name = ""
        # self.attrs: ProjectComponentAttrsBase
        if not hasattr(self, "__belong2__"):
            self.__belong2__ = {}

        super(ProjectComponent, self).__init__(project_ref)

    def set(
        self,
        name: str,
        value,
        escape=None,
        executed_constraints=None,
        head=True,
    ):
        """Set method. Can set any leaf on the attribute tree.

        Args:
            name (str): The key.

            value (Any): The val.

            escape (list): If `'*'` in escape, no constrain will be checked. Otherwise,
            any key in escape will be ignored while checking constrains. Defaults to [].

            executed_constraints (dict): Prevent repeat checking.

        Returns:
            self. Return self of point-style coding.
        """
        assert isinstance(
            name, str
        ), f"{self.__class__.__name__} slicer must be str, got {type(name)}:{name}"
        if escape is None:
            escape = []

        if name not in escape:
            escape.append(name)

        if executed_constraints is None:
            executed_constraints = {"pre": [], "post": []}

        if name in ["__dirty__", "__namespace__"] or (
            hasattr(self, name) and isinstance(getattr(self, name), property)
        ):
            super().__setattr__(name, value)
            return self

        self.__dict__["__dirty__"] = True

        pre_set_attribute(escape, name, executed_constraints, self)

        # Component root
        if hasattr(self, name) and name not in ["type"]:
            setattr(self, name, value)
            flag = True

        else:
            # reproduce
            _, flag = self.attrs.set(
                name, value, escape, executed_constraints, head=False
            )

        if not flag:
            warn_print(
                '\rInput is "{}"\nYou may want to input one of  {} \n'.format(
                    name,
                    nearest_words_with_damerau_levenshtein_distance(
                        self.to_dict(), "".join(name)
                    ),
                )
            )

        one_time_check(escape, name, self)
        post_set_attribute(escape, name, executed_constraints, self)

        self.__dict__["__dirty__"] = False
        return self

    def __repr__(self):
        return "*" + self.name + "*" + ": " + super().__repr__()

    def get(self, name, silent=False):
        """Get method. Can get any leaf on the attribute tree.

        Args:
            name (str): The _name of the attribute.

            silent (bool, optional): Whether to alert when the key was not found. Defaults to False.

        Returns:
            Any: The value.
        """
        assert isinstance(
            name, str
        ), f"{self.__class__.__name__} slicer must be str, got {type(name)}:{name}"
        if name.startswith("__old__"):
            rname = name[7:]
            return self.__dict__["__old__"][rname]

        if name in dir(self):
            return getattr(self, name)

        return self.attrs.get(name, silent)

    def show_info(self):
        ...

    def adopt_component(self, component):
        """Add component to `children` attribute

        Args:
            component (ProjectComponent): A component.
        """
        self.children.append(component)

    def sync_spatial(self, other):
        # Config.DisableConstraints = True
        for attr in [
            "x_min",
            "x_max",
            "x",
            "x_span",
            "y_min",
            "y_max",
            "y",
            "y_span",
            "z_min",
            "z_max",
            "z",
            "z_span",
            "rotate_z",
        ]:
            if (attr in self.attrs) and (attr in other.attrs):
                val = other.get(attr)
                self.attrs.set(attr, val, escape=["*"])

        if "monitor_type" in self and "monitor_type" in other:
            val = other.get("monitor_type")
            if isinstance(val, Macro):
                self.set("monitor_type", val)
        # Config.DisableConstraints = False


class Structure(ProjectComponent):
    ...


class Simulation(ProjectComponent):
    ...


class Port(ProjectComponent):
    def __align__(self, project):
        raise NotImplementedError()


class PortGroup(ProjectComponent):
    ...


class Solver(ProjectComponent):
    ...


class Monitor(ProjectComponent):
    def set_as_sweep_result_monitor(self, name, component):
        from maxoptics.core.project.ProjectBase import get_component_with_class

        project = self.__parent_ref__()
        _, sweep = get_component_with_class(SweepBase, project)
        if not sweep:
            raise IndexError("No Sweep is found in current project")

        sweep.append_result_monitor(name, self, component)

        return self


class SweepBase(ProjectComponent):
    def append_result_monitor(self, *args):
        pass


class Source(ProjectComponent):
    ...


class OtherComponent(ProjectComponent):
    ...


class EmptyComponent(ProjectComponent):
    """A `ProjectComponent` that `__bool__` returns `False`."""

    def __init__(self, project, intended=False):
        super().__init__(weakref.ref(project))
        if not intended:
            error_print("A empty project is referenced")

    # @abstractmethod
    def run(self, mode="t", task_type=None):
        ...

    def __repr__(self) -> str:
        return (
            "This is a invalid component that will only show up "
            "when a non-existed project component name is referenced"
        )

    def __bool__(self) -> bool:
        return False

    def export(self):
        return None
