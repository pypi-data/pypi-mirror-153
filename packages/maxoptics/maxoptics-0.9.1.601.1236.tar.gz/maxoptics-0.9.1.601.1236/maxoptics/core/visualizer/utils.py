"""The utils module provides some common used methods and decorators for visualizer module"""
import inspect
from collections import defaultdict
from functools import wraps
from math import nan
from operator import itemgetter
from time import sleep
from typing import Any, Callable, Dict, List, Type, Tuple

from maxoptics.config import BASEDIR
from maxoptics.core.logger import error_print, warn_print
from maxoptics.core.utils import fdict, decohints
from maxoptics.core.utils import is_float


@decohints
def postmethod(func: Callable):
    """This decorator will do the post for __wrapped__ function.
     __wrapped__ function should be simply a remapping function.

    Args:
        func (Callable): A `classmethod` of `HttpIO`.

    Raises:
        self.error: `SimulationError`. Contains the error msg returned by octopus.

    Returns:
        Callable: A `classmethod`.
    """

    @wraps(func)
    def wrapper(*args, **kws):
        """Take output of `func(*args, **kwargs)` as `data` of `request.post`.

        Raises:
            self.error: `SimulationError`. Contains the error msg returned by octopus.

        Returns:
            Any: 'result' in Decoded JSON.
        """
        self, *args = args

        if "status" in self.__dict__ and self.status == -2:
            raise self.error

        if self.status == -1 or self.id == 0:
            warn_print("Task was aborted! Blank result will be returned.")
            sleep(2)
            return {
                "data": [[nan, nan, nan], [nan, nan, nan], [nan, nan, nan]],
                "columns": [1, 2, 3],
                "header": [1, 2, 3],
                "index": [1, 2, 3],
                "horizontal": [1, 2, 3],
                "vertical": [1, 2, 3],
                "dWidth": [1, 2, 3],
                "dHeight": [1, 2, 3],
            }

        # Check whether fit the args
        # TODO: Network dependent.
        result = self.post(url=func.__name__, **func(self, *args, **kws))
        if result.get("success") is False:
            error_print(func.__name__, " request failed")
            error_print("Incorrect response:", result)
            error_print("Data: ", func(self, *args, **kws))
            assert result.get(
                "success"
            ), f"Please view {BASEDIR / 'var' / 'log' / 'maxoptics.log'}"

        return result["result"]

    return wrapper


@decohints
def coordinate2indexmethod(
    source_func: Callable, check_params=True
) -> Callable:
    """Only for WhaleClient's classmethod.
    Will interpreter string "coordinate" (like `x="0.1"`) to real position in the structure
    and transform them into index.

    Args:
        source_func (Callable): A function as source of needed data. Usually `..._option` method.
        check_params (): passive_eme_sweep_chart has irregular param.

    Returns:
        Callable: Still a decorator.
    """

    def __coordinate2index(func: Callable) -> Callable:
        """This method will decorate given function.

        Args:
            func (Callable): Goal function. As suggested, must be classmethod.

        Returns:
            Callable: Wrapped function.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """The Wrapper."""

            def __mapper(
                dimension_kwargs: Dict[str, Any], coordinates: Dict[str, Any]
            ) -> Dict[str, float]:
                """Remap coordinate.

                Args:
                    dimension_kwargs (Dict[str, Any]): key-word arguments like x, y, z, mode, wavelength.

                    coordinates (Dict[str, Any]): Result of `source_func`

                Raises:
                    ValueError: Filter arg not legal.
                    IndexError: Not indexable.
                    ValueError: Not remappable.

                Returns:
                    Dict[str, float]: Changed dimension_kwargs.
                """
                # dimensions and coordinates
                dimensions, xs, ys, zs, modes, wavelengths = itemgetter(
                    "dimensions",
                    "monitor_x",
                    "monitor_y",
                    "monitor_z",
                    "mode",
                    "wavelength",
                )(defaultdict(lambda: None, coordinates))

                dimensions = [str(_).lower() for _ in dimensions]

                if check_params:
                    assert not set(dimensions).difference(dimension_kwargs), (
                        "Keyword arguments (slicing args) Dismatch. Got args: {}; "
                        "Needed args: {}".format(
                            set(dimension_kwargs), set(dimensions)
                        )
                    )

                for k, v in dimension_kwargs.items():
                    # # k is not legal
                    # if k not in dimensions:
                    #     raise ValueError(f"{k} filter is given,
                    #     which is not in available dimensions {dimensions}")

                    # v is str and able to convert to float
                    if isinstance(v, str) and (fv := is_float(v)) is not None:

                        vs_str = f"{k}s"
                        if vs_str in [
                            "dimensions",
                            "xs",
                            "ys",
                            "zs",
                            "modes",
                            "wavelengths",
                        ]:
                            value_choice = locals()[vs_str]
                        else:
                            value_choice = coordinates.get(k)

                        # corresponding list can be found.
                        if vs := value_choice:

                            if fv not in vs:
                                raise IndexError(
                                    f"Given {k} = {v} is not interpretable. "
                                    f"Must be indexable in {vs}."
                                )

                            else:
                                dimension_kwargs[k] = vs.index(fv)

                        # corresponding list can not be found.
                        else:
                            raise ValueError(
                                f"If you want to use {k} for filtering, "
                                f"you can only use index as its value."
                            )
                return dimension_kwargs

            def __filter(func_kwargs: Dict[str, Any]):
                """Check arguments.

                Args:
                    func_kwargs (Dict[str, Any]): key-word arguments for `func`

                Raises:
                    ValueError: Invalid argument given.
                """
                attribute, operation, attributes, operations = itemgetter(
                    "attribute", "operation", "attributes", "operations"
                )(defaultdict(list, coordinates))
                attributes = list(set(attribute + attributes))
                operations = list(set(operation + operations))

                lambdas = {
                    "attribute": lambda _, cole=attributes: (
                        _ in cole,
                        f"The value of `attribute` must be in {cole}, but {_} is given",
                    ),
                    "operation": lambda _, cole=operations: (
                        _ in cole,
                        f"The value of `operation` must be in {cole}, but {_} is given",
                    ),
                }
                for k, v in func_kwargs.items():
                    if lam := lambdas.get(k):
                        passed, err_msg = lam(v)
                        if not passed:
                            raise ValueError(err_msg)

            # main
            func_signature = inspect.signature(func, follow_wrapped=True)
            source_func_args = inspect.signature(
                source_func, follow_wrapped=True
            )

            # transform args to kwargs
            # full_kwargs = {
            #     **kwargs,
            #     **dict(zip(func_signature.parameters, args)),
            # }

            __full_kwargs = func_signature.bind(*args, **kwargs)
            __full_kwargs.apply_defaults()
            full_kwargs = dict(__full_kwargs.arguments)
            full_kwargs.update(**__full_kwargs.kwargs)
            if "kwargs" in full_kwargs:
                full_kwargs.pop("kwargs")

            self = full_kwargs.pop("self")

            # get corresponding kwargs
            func_kwargs = {
                k: v
                for k, v in full_kwargs.items()
                if k in func_signature.parameters
            }
            source_func_kwargs = {
                k: v
                for k, v in full_kwargs.items()
                if k in source_func_args.parameters
            }

            # prepare coordinates
            coordinates = source_func(self, **source_func_kwargs)
            __filter(func_kwargs)

            # prepare dimension_kwargs

            # TODO: simplify
            complement_dimension_kwargs_name = [
                name
                for name, _para in func_signature.parameters.items()
                if _para.kind
                in [
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                ]
                and _para.default
            ]

            dimension_kwargs = {
                k: v
                for k, v in full_kwargs.items()
                if k not in complement_dimension_kwargs_name
            }

            # performs remap
            mapped = __mapper(dimension_kwargs, coordinates)

            # get modified func_kwargs
            func_kwargs = {**func_kwargs, **mapped}

            # execute func
            return func(self, **func_kwargs)

        wrapper.__options_method__ = source_func

        return wrapper

    return __coordinate2index


@decohints
def parsermethod(func: Callable):
    """Transform the result of decorated method to a TaskFile"""
    from maxoptics.core.TaskFile import TaskFile

    @wraps(func)
    def wrapper(*args, **kws):
        self, *__args__ = args
        return TaskFile(
            func(*args, **kws),
            self,
            *__args__,
            **(
                fdict(kws)
                | (
                    dict(
                        zip(
                            inspect.getfullargspec(func).args[::-1],
                            inspect.getfullargspec(func).defaults,
                        )
                    )
                    if bool(inspect.getfullargspec(func).defaults)
                    else {}
                )
            ),
        )

    return wrapper


@decohints
def indexer(func: Callable):
    """Transform the result of decorated method to a TaskFile"""

    @wraps(func)
    def wrapper(*args, **kws):
        ret = func(*args, **kws)
        ret["dWidth"] = list(range(len(ret["dWidth"])))
        ret["dHeight"] = list(range(len(ret["dHeight"])))
        return ret

    return wrapper


@decohints
def bind_target_selections(*selections: List[str]):
    """Bind a parameters checker of `target` to a visualizer method"""

    def closure(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func, follow_wrapped=True)
            sig_ar = sig.bind(*args, **kwargs)
            target = sig_ar.arguments["target"]
            assert (
                target in selections
            ), f"Method {func} can not read {target} that is not in {selections}"
            return func(*args, **kwargs)

        wrapper.__target_selections__ = selections
        return wrapper

    return closure


@decohints
def bind_monitor_types(*monitor_types: Tuple[Type]):
    """Bind a parameters checker of `monitor` to a visualizer method."""

    def closure(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func, follow_wrapped=True)
            sig_ar = sig.bind(*args, **kwargs)
            monitor = sig_ar.arguments["monitor"]
            if not isinstance(monitor, int):
                assert isinstance(
                    monitor, monitor_types
                ), f"Method {func} can not accept {monitor.__class__}: {monitor}"
            return func(*args, **kwargs)

        wrapper.__monitor_types__ = monitor_types

        return wrapper

    return closure
