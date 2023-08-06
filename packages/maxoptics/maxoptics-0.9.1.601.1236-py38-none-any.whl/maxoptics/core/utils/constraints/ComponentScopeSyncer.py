"""The ComponentScopeSyncer module provides support of attribute synchronizing in a single component."""
from collections import defaultdict
from inspect import getfullargspec

from maxoptics.core.logger import info_print
from maxoptics.var.config import Config
from maxoptics.var.constraints import component_scope


def excute_one(escape, functor, obj, args, arg_values, to):
    """Syncornize one attribute in obj.

    Args:
        escape (list[str]): Attributes in `escape` would not be changed by
        derivative component-scope synchronizing actions.

        functor (Callable): A method that can describe action of current synchronizing.

        obj (ProjectComponent): The component to be changed.

        args (list[str]): A list of args name.

        arg_values (list[Any]): The list of values corresponding to 'args'.

        to (str): The attribute's name that will be changed.

    Return:
        None
    """

    res = functor(obj, *arg_values)

    if to:
        if Config.Verbose:
            with info_print(f"{to} = {res}"):
                obj.set(to, res, escape=escape + args + [to])
        else:
            obj.set(to, res, escape=escape + args + [to])


class Restrainer:
    def __init__(self):
        self.hkts = component_scope()
        self.trigger_map = defaultdict(list)
        for _, functor in self.hkts:
            args = getfullargspec(functor).args
            args = args[1:]
            for arg in args:
                if functor not in self.trigger_map[arg]:
                    self.trigger_map[arg].append((_, functor))

        self.trigger_map = dict(self.trigger_map)

    def check(self, obj, key, escape):
        filtered_hkts = []
        if hasattr(obj, "name"):
            obj_repr = obj.name
        else:
            obj_repr = obj

        if key not in self.trigger_map:
            return
        if Config.DisableConstraints:
            hkts = []
        else:
            hkts = self.trigger_map[key]

        for to, functor in hkts:
            if to in escape or "*" in escape:
                ...
            else:
                if to in obj:
                    args = getfullargspec(functor).args
                    args = args[1:]
                    arg_values = []
                    for _ in args:
                        if _ not in obj:
                            break
                        else:
                            arg_values.append(obj.get(_))

                    if len(arg_values) < len(args):
                        continue

                    filtered_hkts.append((to, functor, args, arg_values))

        if filtered_hkts:
            if Config.Verbose:
                with info_print(
                    f"(CC) {obj_repr}: {key} is set as {obj.get(key)}."
                ):
                    for to, functor, args, arg_values in filtered_hkts:
                        excute_one(escape, functor, obj, args, arg_values, to)

            else:
                for to, functor, args, arg_values in filtered_hkts:
                    excute_one(escape, functor, obj, args, arg_values, to)
