import inspect
from collections import defaultdict
from typing import Any, Dict, Iterable, List, TypeVar, Union

import yaml

from maxoptics.config import Config
from maxoptics.core.abc import Exportable
from maxoptics.core.error import ProjectBuildError
from maxoptics.core.logger import (
    error_print,
    info_print,
)

from maxoptics.core.utils.constraints import cr, pr
from maxoptics.core.utils.currying import Currying
from maxoptics.macros import get_namespace

T = TypeVar("T")

default_default_dict = defaultdict(dict)


class FP:
    """FP?"""

    def apply(self, functor):
        """FP"""
        if isinstance(functor, Currying):
            fun = functor.func
        else:
            fun = functor

        # No longer useful
        if "_" in (inspect.getfullargspec(fun).kwonlydefaults or {}):
            return functor(_=self) or self
        else:
            return functor(self) or self

    def __lshift__(self, other):
        __self__ = self
        if isinstance(other, Iterable):
            for action in other:
                __self__ = __self__.apply(action)
        else:
            __self__ = __self__.apply(other)
        return __self__


class Expression:
    """Provide nice management for expression."""

    def __init__(self, attr):
        from maxoptics.core.component.base.Attrs import (
            ProjectComponentAttrsBase,
        )

        self.__store = {}
        self.__attr__: ProjectComponentAttrsBase = attr
        self.__initialized__ = False

    @property
    def __document__(self):
        return self.__attr__.__parent_ref__().__parent_ref__().DOCUMENT

    def __setattr__(self, key, value):
        """Sync to attributes in `attrs`

        Args:
            key (str): The key
            value (str): The expression.

        Returns:
            None
        """
        if hasattr(self, "__initialized__"):
            self.__store[key] = value
            super().__setattr__(key, value)
            if not Config.DisableConstraints:
                real_val = self.__attrs_dict__[key]
                self.__attr__[key] = real_val

        else:
            super(Expression, self).__setattr__(key, value)

    def __to_dict__(self):
        """Full output"""
        return {**self.__expre_dict__, **self.__attrs_dict__}

    @property
    def __expre_dict__(self):
        """Output stored expressions"""
        return {f"expre_{key}": val for key, val in self.__store.items()}

    @property
    def __attrs_dict__(self):
        """Output calculated values"""

        # Fetch and classify Params
        variables = self.__document__.attrs.configGlobleParam

        def is_mutable_key_values(v):
            if v["globleParamExp"].strip() != "":
                return True
            else:
                return False

        mutable_key_values = [v for v in variables if is_mutable_key_values(v)]
        immutable_key_values = [
            v for v in variables if not is_mutable_key_values(v)
        ]

        # Parse Expression
        ikv = {}
        mkv = {}

        def meval(exp):
            return eval(exp, __import__("math").__dict__, {**ikv, **mkv})

        for va in immutable_key_values:
            key = va["globleParamKey"]
            val = va["globleParamValue"]
            try:
                ikv[key] = float(val)
            except Exception:
                ikv[key] = val

        count = 0  # Prevent inf loop
        err = ValueError("Unknown error")  # Default error
        err_exp = ""

        while len(mkv) < len(mutable_key_values):
            for va in mutable_key_values:
                key = va["globleParamKey"]
                exp = va["globleParamExp"]
                if key in mkv:
                    continue

                try:
                    val = meval(exp)
                    try:
                        mkv[key] = float(val)
                    except Exception:
                        mkv[key] = val
                except NameError as e:
                    err = e
                    err_exp = exp
                except Exception as e:
                    error_print(f"Handling Expression {exp} failed")
                    raise e

            if count > len(mutable_key_values):
                error_print(f"Handling Expression {err_exp} failed")
                raise err
            count += 1

        # Eval expressions
        exs = self.__store

        ret = {}
        for ex, exv in exs.items():
            try:
                ret[ex] = meval(exv)
            except Exception as e:
                # print(self.__store)
                error_print(f"Failed to eval expression: {exv} ({ex})")
                raise e

        return ret


class StyleBase(FP, Exportable):
    def __init__(self, reference=None):
        """Initialize basic attributes."""
        self.__dirty__ = None
        self.__parent_ref__ = reference
        if Config.Debug:
            assert reference() is not self
        self.__old__ = {}
        self.__namespace__ = {}

        from maxoptics.core.component.base.Attrs import (  # noqa
            ProjectComponentAttrsBase,
        )

        if isinstance(self, ProjectComponentAttrsBase):
            self.__expre__ = Expression(self)

    @property
    def export(self):
        """For generate a project tree.
        This is a self-changing method, be caution about infinite loop.

        Returns:
            dict: dict_form of self
        """

        if hasattr(self, "__expre__"):
            expressions = self.__expre__
            if not Config.DisableConstraints:
                attrs_dict = expressions.__attrs_dict__
            else:
                attrs_dict = {}
            expre_dict = expressions.__expre_dict__
            self.update(**attrs_dict)

            # Not Good
            comp = self.__parent_ref__()
            project = comp.__parent_ref__()
            doc = project.DOCUMENT
            if expressions.__expre_dict__:
                if comp.id not in doc.attrs.exp_obj:
                    doc.attrs.exp_obj[comp.id] = {}
                doc.attrs.exp_obj[comp.id].update(expressions.__expre_dict__)

        ret = self.to_dict(export=True)

        if isinstance(ret, Exception):
            return ProjectBuildError(self, str(ret))

        if hasattr(self, "__expre__"):
            ret.update(**expre_dict)

        return ret

    def to_dict(self, extract_dict=None, extract_all=True, export=False):
        """
        Tidy up attributes and form a dictionary.

        Returns:
            dict (dict): A serializable object for output.
        """

        if extract_dict is None:
            extract_dict = default_default_dict

        result = dict(self.__dict__)

        # pop out builtin attrs
        for k in list(result.keys()):
            if k.startswith("__") or k in [
                "showInfo",
                "_abc_impl",
                "_objLink",
            ]:
                result.pop(k)

        if hasattr(self, "__namespace__"):
            __namespace__ = get_namespace(
                self.__class__.__name__, self.__namespace__
            )
        else:
            __namespace__ = get_namespace(self.__class__.__name__)

        result = clean(
            result, extract_dict, extract_all, export, __namespace__
        )
        if isinstance(result, Exception):
            return result

        return result

    def __contains__(self, item):
        if isinstance(item, str):
            ans = self.get(item, silent=True)
            if ans is not None:
                return True
            else:
                return False

        raise NotImplementedError(
            f"The contains-check between {self.__class__} and {type(item)} is not implemented"
        )

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def set(self, *args, **kwargs):
        raise NotImplementedError()

    def update(self, *args, **kwargs):
        """Just like `dict.update`."""
        for arg in args:
            if not isinstance(arg, dict):
                error_print("Wrong input type !!! Dict needed")
                self.__dirty__ = True
                return
            else:
                kwargs.update(arg)
        for key in kwargs:
            self.set(key, kwargs[key])
        return self

    def __or__(self, other):
        return self.update(other)

    def __call__(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def __getitem__(self, name) -> Any:
        """Alias of `get`

        Args:
            name (str): Key.

        Returns:
            Any: Value.
        """
        return self.get(name, silent=False)

    def __setitem__(self, name: str, value: Any):
        """Alias of `set`

        Args:
            name (str): Key.

            value (Any): Value.
        Returns:
            None.
        """
        return self.set(name, value)

    def check_status(self):
        return self.__dirty__

    def list_all_dict(self, dict_a, level):
        """
        Print the __dict__ as a tree form
        """
        level += 1
        if isinstance(dict_a, dict):
            # if level != 1:
            print("")
            for x in range(len(dict_a)):
                temp_key = list(dict_a.keys())[x]
                info_print("-" * 3 * level + ">", end=" ")
                info_print(temp_key, end=" ")
                print(":", end=" ")
                temp_value = dict_a[temp_key]
                self.list_all_dict(temp_value, level)
        elif isinstance(dict_a, list):
            if len(dict_a) == 0:
                print("[]")
            for x in range(len(dict_a)):
                self.list_all_dict(dict_a[x], level)
            print("")
        else:
            # print(dict_a)
            pass

    def __tree_repr__(self) -> str:
        __repr = self.__repr__()
        key_values = self.to_dict()
        if isinstance(key_values, Exception):
            raise key_values

        return (
            __repr + "\n" + yaml.dump(key_values, Dumper=yaml.SafeDumper)
        ).replace("\n", "\n    ")

    def __dataclass__repr__(self, extract_dict, extract_all) -> str:
        key_values = self.to_dict(
            extract_dict=extract_dict, extract_all=extract_all
        )
        if isinstance(key_values, Exception):
            raise key_values

        return "{class_name}({key_value_str})".format(
            class_name=self.__class__.__name__,
            key_value_str=", ".join(
                f"{key}={value}" for key, value in key_values.items()
            ),
        )


def clean(
    dikt: dict,
    extract_dict: Dict[str, Union[str, Dict]],
    extract_all: bool,
    export: bool,
    namespace: Dict,
):
    """
    Remove excrescent key-value. Transform components in `children` into dictionaries too.

    Args:
        dikt (dict): The dict to be clean.

        extract_all (bool): Whether to extract blindly

        extract_dict (DefaultDict):

    Returns:
        dict: The cleaned dict.
    """
    # Remove built-in attribute.
    for key in list(dikt.keys()):
        if key.startswith("__") or key == "showInfo" or key == "_abc_impl":
            dikt.pop(key)

    for key, value in dikt.items():

        extract_flag = key in extract_dict or extract_all

        extract_dict_ = {}
        extract_all_ = extract_all
        if not extract_all:
            extract_dict_ = extract_dict.get(key, {})
            extract_all_ = extract_dict_ == "*"

        if isinstance(value, (Exportable, list, tuple)) and extract_flag:

            if isinstance(value, Exportable):
                if export:
                    value.__namespace__ = namespace
                    r = value.export
                    if isinstance(r, Exception):
                        return r
                    dikt[key] = r
                else:
                    dikt[key] = value.to_dict(extract_dict_, extract_all_)

            elif isinstance(value, list):
                try:
                    if export:
                        ret = []
                        for _ in value:
                            _.__namespace__ = namespace
                            r = _.export
                            if isinstance(r, Exception):
                                return r
                            ret.append(r)
                        dikt[key] = ret
                    else:
                        dikt[key] = [
                            _.to_dict(extract_dict_, extract_all_)
                            for _ in value
                        ]
                except (KeyError, TypeError, AttributeError):
                    pass

    return dikt


def pre_set_attribute(
    escape: List, name: str, executed_constraints, self: StyleBase
) -> StyleBase:
    from maxoptics.var.project import MosProject

    maybe_project = self
    emit_list = []
    attribute_name = name
    posted = executed_constraints["pre"]

    while not isinstance(maybe_project, MosProject):
        component_type = maybe_project.__class__.__name__
        signals = [
            f"{component_type}PreSet__{attribute_name}",
            f"{component_type}PreSet__...",
            f"{component_type}PreSet__...",
        ]
        for sig in signals:
            if sig not in posted:
                posted.append(sig)
                emit_list.append((sig, maybe_project))

        maybe_project = maybe_project.__parent_ref__()

    project = maybe_project

    for sig, comp in emit_list:
        pr().emit(project, sig, comp)

    return self


def post_set_attribute(
    escape: List, name: str, executed_constraints, self: StyleBase
) -> StyleBase:
    from maxoptics.var.project import MosProject

    maybe_project = self
    emit_list = []
    attribute_name = name
    posted = executed_constraints["post"]

    while not isinstance(maybe_project, MosProject):
        component_type = maybe_project.__class__.__name__
        signals = [
            f"{component_type}PostSet__{attribute_name}",
            f"{component_type}PostSet__...",
            f"{component_type}PostSet__...",
        ]
        for sig in signals:
            if sig not in posted:
                posted.append(sig)
                emit_list.append((sig, maybe_project))

        maybe_project = maybe_project.__parent_ref__()

    project = maybe_project

    for sig, comp in emit_list:
        pr().emit(project, sig, comp)

    return self


def one_time_check(escape, name, self):
    # Must be on component level
    cr().check(self, name, escape)
