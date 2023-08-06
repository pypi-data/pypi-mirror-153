# coding=utf-8
"""This module provides utilities used frequently by other modules."""
import inspect
import os
import re
import sys
import warnings
from collections import defaultdict
from pathlib import Path
from typing import Any, Union, List, Dict, Callable


class ShadowAttr:
    def __new__(cls, _key="", *args):
        def getter(self):
            key = _key
            return self.get(key)

        def setter(self, value):
            key = _key
            return self.set(key, value)

        def deleter(self):
            key = _key
            exec(f"del self.{key}")

        return property(fget=getter, fset=setter)


def damerau_levenshtein_distance(s1, s2):
    # From jellyfish
    len1 = len(s1)
    len2 = len(s2)
    infinite = len1 + len2

    # character array
    da = defaultdict(int)

    # distance matrix
    score = [[0] * (len2 + 2) for x in range(len1 + 2)]

    score[0][0] = infinite
    for i in range(0, len1 + 1):
        score[i + 1][0] = infinite
        score[i + 1][1] = i
    for i in range(0, len2 + 1):
        score[0][i + 1] = infinite
        score[1][i + 1] = i

    for i in range(1, len1 + 1):
        db = 0
        for j in range(1, len2 + 1):
            i1 = da[s2[j - 1]]
            j1 = db
            cost = 1
            if s1[i - 1] == s2[j - 1]:
                cost = 0
                db = j

            score[i + 1][j + 1] = min(
                score[i][j] + cost,
                score[i + 1][j] + 1,
                score[i][j + 1] + 1,
                score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1),
            )
        da[s1[i - 1]] = i

    return score[len1 + 1][len2 + 1]


def nearest_words_with_damerau_levenshtein_distance(dic, name):
    def extract_dict(mapping: Dict, list_of_name: List):
        for key_name in mapping:
            if key_name not in list_of_name:
                list_of_name.append(key_name)
            if isinstance(mapping[key_name], dict):
                extract_dict(mapping[key_name], list_of_name)
        return list_of_name

    if isinstance(dic, dict):
        name_list = extract_dict(dic, [])
    elif isinstance(dic, list):
        name_list = dic
    else:
        raise SystemError("SDK down.")
    dis_list = []
    result_list = []
    for n in name_list:
        dis = damerau_levenshtein_distance(n, name)
        dis_list.append(dis)
        result_list.append(n)

    sorted_zipped = sorted(zip(dis_list, result_list))
    sorted_unzipped = tuple(zip(*sorted_zipped))[1][:5]
    return sorted_unzipped


def is_float(value: Any) -> Union[float, None]:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def find_maxoptics_conf():
    try:
        __MainPath__ = Path(
            inspect.getfile(sys.modules.get("__main__"))
        ).parent
        conf_name = "maxoptics.conf"
        if os.path.exists(__MainPath__ / conf_name):
            __ConfigPath__ = __MainPath__ / conf_name
        elif os.path.exists(__MainPath__.parent / conf_name):
            __ConfigPath__ = __MainPath__.parent / conf_name
        elif os.path.exists(__MainPath__.parent.parent / conf_name):
            __ConfigPath__ = __MainPath__.parent.parent / conf_name
        else:
            ind = list(sys.modules.keys()).index("maxoptics")
            secondary_path = Path(
                inspect.getfile(list(sys.modules.values())[ind - 1])
            )
            if os.path.exists(secondary_path.parent / conf_name):
                __ConfigPath__ = secondary_path.parent / conf_name
            elif os.path.exists(secondary_path.parent.parent / conf_name):
                __ConfigPath__ = secondary_path.parent.parent / conf_name
            elif os.path.exists(
                secondary_path.parent.parent.parent / conf_name
            ):
                __ConfigPath__ = (
                    secondary_path.parent.parent.parent / conf_name
                )
            else:
                __ConfigPath__ = Path(".")

    except (AttributeError, TypeError) as e:  # noqa
        warnings.warn(
            "No __main__ modules found, using the default configuration"
        )
        __ConfigPath__ = Path(".")
        __MainPath__ = Path(".")

    return __MainPath__, __ConfigPath__


def decohints(decorator: Callable) -> Callable:
    """To fix the strange problem of Pycharm"""
    return decorator


if sys.version_info.minor >= 9:
    fdict = dict
    fstr = str

else:

    class fdict(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __or__(self, incoming):
            # assert isinstance(incoming, self.__class__)
            # for arg in args:
            # assert isinstance(arg, self.__class__)
            self.update(incoming)
            return self

    class fstr(str):
        def __init__(self, obj):
            self.__str__ = obj
            super().__init__()

        def removesuffix(self, suffix):
            len_of_suffix = len(suffix)
            if len(self) < len_of_suffix:
                return self
            else:
                if self[-len_of_suffix:] == suffix:
                    return fstr(self[:-len_of_suffix])
                else:
                    return self

        def removeprefix(self, prefix: str):
            len_of_prefix = len(prefix)
            if len(self) < len_of_prefix:
                return self
            else:
                if self[:len_of_prefix] == prefix:
                    return fstr(self[len_of_prefix:])
                else:
                    return self


def removeprefix(self: str, prefix: str):
    assert isinstance(prefix, str)
    len_of_prefix = len(prefix)
    if len(self) < len_of_prefix:
        return self
    else:
        if self[:len_of_prefix] == prefix:
            return self[len_of_prefix:]
        else:
            return self


def removesuffix(self: str, suffix: str):
    assert isinstance(suffix, str)
    len_of_suffix = len(suffix)
    if len(self) < len_of_suffix:
        return self
    else:
        if self[-len_of_suffix:] == suffix:
            return self[:-len_of_suffix]
        else:
            return self
