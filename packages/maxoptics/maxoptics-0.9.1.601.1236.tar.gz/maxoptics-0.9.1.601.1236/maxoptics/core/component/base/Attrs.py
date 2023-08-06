from typing import TypeVar, List

from maxoptics.core.component.base.base import (
    StyleBase,
    pre_set_attribute,
    one_time_check,
    post_set_attribute,
)
from maxoptics.core.logger import warn_print
from maxoptics.core.utils import (
    removeprefix,
    nearest_words_with_damerau_levenshtein_distance,
)

T = TypeVar("T")


class ProjectComponentAttrsBase(StyleBase):
    def __init__(self, component_ref):
        super(ProjectComponentAttrsBase, self).__init__(component_ref)
        self.__fully_initialized__ = True

    def __setattr__(self, name, value):
        """Alias of `set`

        Args:
            name (str): Key.

            value (Any): Value.

        Returns:
            None.
        """
        if (
            hasattr(self, "__fully_initialized__")
            and self.__fully_initialized__
        ):
            self.set(name, value)
        else:
            super().__setattr__(name, value)

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

        dikt = self.to_dict()
        if isinstance(dikt, Exception):
            raise dikt

        def __extract(origin, _name):
            nonlocal flag
            next_layer: List[dict] = [origin]
            ret = None
            while next_layer:
                this_layer = next_layer
                next_layer = []
                for dic in this_layer:
                    if _name in dic:
                        ret = ret or dic[_name]
                    for v in dic.values():
                        if isinstance(v, dict):
                            next_layer.append(v)
                        if isinstance(v, StyleBase):
                            next_layer.append(v.__dict__)
            if ret is None:
                flag = False
            return ret

        flag = True
        res = __extract(dikt, name)

        if flag:
            return res
        else:
            if silent:
                return
            else:
                raise KeyError(
                    "A Invalid value retrieval, inputs are {}".format(name)
                )

    def __repr__(self):
        return (
            "*"
            + self.__parent_ref__().name
            + "*"
            + ".attrs...: "
            + super().__repr__()
        )

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

        if (due_underscore_start := name.startswith("__expre__")) or (
            expre_start := name.startswith("expre_")
        ):
            if due_underscore_start:
                rname = removeprefix(name, "__expre__")
            elif expre_start:
                rname = removeprefix(name, "expre_")

            setattr(self.__expre__, rname, value)
            return self, True

        if name in ["__dirty__", "__namespace__"] or (
            hasattr(self, name) and isinstance(getattr(self, name), property)
        ):
            super().__setattr__(name, value)
            return self, True

        self.__dict__["__dirty__"] = True

        pre_set_attribute(escape, name, executed_constraints, self)

        # Component attrs
        if hasattr(self, name):
            # Component's __setattr__ was overwritten
            super().__setattr__(name, value)
            flag = True
            post_set_attribute(escape, name, executed_constraints, self)
        else:
            flag = False

        # reproduce
        for key, obj in self.__dict__.items():
            if isinstance(obj, ProjectComponentAttrsBase):
                _, ret = obj.set(
                    name, value, escape, executed_constraints, head=False
                )
                flag = ret or flag

        if head is True:
            if not flag:
                warn_print(
                    '\rInput is "{}"\nYou may want to input one of  {} \n'.format(
                        name,
                        nearest_words_with_damerau_levenshtein_distance(
                            self.to_dict(), "".join(name)
                        ),
                    )
                )
            else:
                one_time_check(escape, name, self.__parent_ref__())

        self.__dict__["__dirty__"] = False
        return self, flag

    def __lazy_attr__(self, functor):
        class A:
            def __init__(self, ss):
                self.ss = ss

            @property
            def export(self):
                return functor(self.ss)

        return A(self)
