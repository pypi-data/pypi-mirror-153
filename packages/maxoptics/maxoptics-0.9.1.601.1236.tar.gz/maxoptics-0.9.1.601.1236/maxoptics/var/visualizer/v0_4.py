import inspect
from functools import lru_cache, partial, wraps
from inspect import signature, Parameter, Signature
from operator import itemgetter
from pprint import pprint  # noqa
from typing import Callable, Dict, Any, Optional, Union, List

from maxoptics.core.utils import removeprefix, decohints
from maxoptics.var.models import (
    ProfileMonitor,
    TimeMonitor,
    PowerMonitor,
    IndexMonitor,
)
from maxoptics.core.component.base.Component import ProjectComponent
from maxoptics.var.MosIO import WhaleClients
from maxoptics.core.TaskFile import TaskFile
from maxoptics.core.visualizer.common import standard_chart, standard_option
from maxoptics.core.visualizer.utils import (
    postmethod,
    parsermethod,
    coordinate2indexmethod,
    bind_monitor_types,
    bind_target_selections,
    indexer,
)


class V04API(WhaleClients):
    api_version = "0.4"

    def fields(self):
        raise NotImplementedError()

    def dump_all(self):
        raise NotImplementedError()

    def sync_download(self):
        raise NotImplementedError()

    @staticmethod
    def auto_fill(
        method: Callable,
        targets: List[str],
        monitor: Optional[ProjectComponent] = None,
    ):
        options_method = method.__options_method__
        target_selections = method.__target_selections__

        args, options_method_args = (
            inspect.getfullargspec(method).args,
            inspect.getfullargspec(options_method).args,
        )

        if "monitor" in args and "monitor" in options_method_args:
            assert (
                monitor
            ), f"The method {method} requires monitor arg, which is not"
            options_method = partial(options_method, monitor=monitor)

        for target in set(targets).intersection(target_selections):

            options = options_method(target)

            for params in options2params(target, options):

                kwargs = params2kwargs(method, **params)
                if monitor:
                    kwargs["monitor"] = monitor

                yield method, kwargs

    @classmethod
    def quick_view(
        cls, project, targets=["intensity", "line", "table"], *methods
    ):
        monitors_and_ports = project.monitors + project.ports

        for method in methods:
            if not hasattr(method, "__monitor_types__"):
                yield from cls.auto_fill(method, targets)
            else:
                for viewable in monitors_and_ports:
                    if isinstance(viewable, method.__monitor_types__):
                        yield from cls.auto_fill(method, targets, viewable)


class V04FDEResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(project, targets, self.passive_fde_result_chart)

    @lru_cache(maxsize=None)
    @postmethod
    @bind_target_selections("intensity", "table")
    def passive_fde_options(self, target: str):
        """Get FDE Mode Solver arguments' options.

        Args:
            target (str): The Options: table, intensity

        Returns:
            Dict[str, Any]: options [key, options].
        """
        monitor = 0
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fde_options)
    @bind_target_selections("intensity", "table")
    def passive_fde_result_chart(
        self,
        target: str,
        attribute: str,
        operation: str,
        x=0,
        y=0,
        z=0,
        mode=0,
        log=False,
    ) -> TaskFile:
        r"""Get FDE Mode Solver Result.

        Args:
            target (str): The Options: table, intensity.

            attribute (str): The Options: E, Ex, Ey, Ez, H, Hx, Hy, Hz, Px, Py, Pz, Energy density.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            x (str|int): index or real value.

            y (str|int): index or real value.

            z (str|int): index or real value.

            mode (str|int): index or real value.

        Returns:
            TaskFile: A general result handler.
        """

        # TODO: Why hasn't this problem been solved?
        kwargs = dict(x=x, y=y, z=z, mode=mode)
        for k, v in kwargs.items():
            if v == "plotX":
                kwargs[k] = "plotx"
            if v == "plotY":
                kwargs[k] = "ploty"

        # TODO: monitor is not a valid input
        monitor = 0
        result = standard_chart(locals())
        return result


class V04FDESweepResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(project, targets, self.passive_fde_sweep_chart)

    @lru_cache(maxsize=None)
    @postmethod
    @bind_target_selections("polyline")
    def passive_fde_sweep_options(self, target: str) -> Dict[str, Any]:
        """Get FDE Sweep arguments' options.

        Args:
            target (str): The Options: polyline

        Returns:
            Dict[str, Any]: options [key, options].
        """
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fde_sweep_options)
    @bind_target_selections("polyline")
    def passive_fde_sweep_chart(
        self, target: str, attribute: str, log=False, **kwargs
    ) -> TaskFile:
        r"""Get FDE Sweep result.

        Args:
            target (str): The Options: polyline
            attribute (str): The Options: effective index, group index, loss, fraction

        Returns:
            TaskFile: A general result handler.
        """

        return {
            "target": target,
            "pub": {"taskId": self.task_id, "attribute": attribute},  # pub
            "option": kwargs,
        }


class V04EMEResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(
            project,
            targets,
            self.passive_eme_monitor_chart,
            self.passive_eme_smatrix_chart,
        )

    @lru_cache(maxsize=None)
    @postmethod
    @bind_monitor_types(ProfileMonitor)
    @bind_target_selections("intensity", "line")
    def passive_eme_monitor_option(
        self, target: str, monitor: Union[int, ProjectComponent]
    ) -> Dict[str, Any]:
        """Get EME arguments' options.

        Args:
            target (str): The Options: intensity, line.
            monitor (int|MonitorLike): The goal monitor's index or monitor object.

        Returns:
            Dict[str, Any]: Options [str, option]
        """
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_eme_monitor_option)
    @bind_monitor_types(ProfileMonitor)
    @bind_target_selections("intensity", "line")
    def passive_eme_monitor_chart(
        self,
        target: str,
        monitor: Union[int, ProjectComponent],
        attribute: str,
        operation: str,
        log=False,
        x=0,
        y=0,
        z=0,
    ):
        """

        Args:
            target (str): The Options: intensity, line.

            monitor (int|MonitorLike): The goal monitor's index or monitor object.

            attribute (str): The Options: E, Ex, Ey, Ez, H, Hx, Hy, Hz, Px, Py, Pz, Energy density.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            x (str|int): index or real value.

            y (str|int): index or real value.

            z (str|int): index or real value.

        Returns:

        """
        kwargs = dict(x=x, y=y, z=z)
        return standard_chart(locals())

    @lru_cache(maxsize=None)
    @postmethod
    # @bind_target_selections("intensity")
    def passive_eme_smatrix_option(self, target: str) -> Dict[str, Any]:
        """Get EME Smatrix arguments' options

        Args:
            target (str): The only option: intensity

        Returns:
            Dict[str, Any]: options [key, options].
        """
        target = "intensity"
        return standard_option(locals())

    @parsermethod
    @indexer
    @postmethod
    @coordinate2indexmethod(passive_eme_smatrix_option)
    # @bind_target_selections("intensity")
    def passive_eme_smatrix_chart(
        self,
        target: str,
        attribute: str,
        operation: str,
        log=False,
    ) -> TaskFile:
        r"""Get EME Sweep Result.

        Args:
            target (str): The only option: intensity.

            attribute (str): The only option: S.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

        Returns:
            TaskFile: A general result handler.
        """
        target = "intensity"
        kwargs = {}
        return standard_chart(locals())


class V04EMEParameterSweepResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(
            project,
            targets,
            self.passive_eme_monitor_chart,
        )

    @lru_cache(maxsize=None)
    @postmethod
    @bind_target_selections("intensity")
    def passive_eme_params_sweep_option(self, target: str) -> Dict[str, Any]:
        """Get EME Parameter sweep arguments' options.

        Args:
            target (str): The Options: intensity, line.

        Returns:
            Dict[str, Any]: Options [str, option]
        """
        monitor = 0
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_eme_params_sweep_option)
    # @bind_monitor_types(ProfileMonitor)
    @bind_target_selections("intensity")
    def passive_eme_params_sweep_chart(
        self,
        target: str,
        attribute: str,
        operation: str,
        log=False,
        **kwargs,
    ):
        """Get EME Parameter sweep result.

        kwargs for sweep dynamic paras.

        Args:
            target (str): The Options: intensity, line.

            attribute (str): The Option: S.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

        Returns:
            TaskResult
        """
        monitor = 0
        return standard_chart(locals())


class V04EMESweepResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(project, targets, self.passive_eme_sweep_chart)

    @lru_cache(maxsize=None)
    @postmethod
    @bind_target_selections("line")
    def passive_eme_sweep_option(self, target: str) -> Dict[str, Any]:
        """Get EME Sweep arguments' options.

        Args:
            target (str): The only option: line.

        Returns:
            Dict[str, Any]: options [key, options].
        """
        monitor = 0
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_eme_sweep_option, check_params=False)
    @bind_target_selections("line")
    def passive_eme_sweep_chart(
        self, target: str, attribute: str, operation: str, **kwargs
    ) -> TaskFile:
        r"""Get EME Sweep Result. `monitor` is not a needed parameter.
        For kwargs, please input Group__span__`n` = 'plotX', n ∈ N.

        Args:
            target (str): The only option: line.

            attribute (str): The only option: S.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            wavelength (str|int): index or real value.

            */*/kwargs: Please input Group__span__`n` = 'plotX', n ∈ N.

        Returns:
            TaskFile: A general result handler.
        """
        monitor = 0
        kwargs = {key.replace("__", " "): val for key, val in kwargs.items()}
        return standard_chart(locals())


class V04FDTDResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(
            project,
            targets,
            self.passive_fdtd_fd_result_chart,
            self.passive_fdtd_td_result_chart,
        )

    @lru_cache(maxsize=None)
    @postmethod
    @bind_monitor_types(PowerMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_fd_result_option(
        self, target: str, monitor: Union[int, ProjectComponent]
    ) -> Dict[str, Any]:
        """Get FDTD FD arguments' options.

        Args:
            target (str): The Options: intensity, line
            monitor (int|MonitorLike): The goal monitor's index or monitor object.

        Returns:
            Dict[str, Any]: Options [key, options]
        """
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fdtd_fd_result_option)
    @bind_monitor_types(PowerMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_fd_result_chart(
        self,
        target: str,
        monitor: Union[int, ProjectComponent],
        attribute: str,
        operation: str,
        log=False,
        x=0,
        y=0,
        z=0,
        wavelength=0,
    ) -> TaskFile:
        r"""Get FDTD FD result.

        Args:
            target (str): The Options: intensity, line.

            monitor (int|MonitorLike): The goal monitor's index or monitor object.

            attribute (str): The Options: E, Ex, Ey, Ez, H, Hx, Hy, Hz, Px, Py, Pz, Energy density, T.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            log (bool): Whether to do log operation on data.

            x (str|int): index or real value.

            y (str|int): index or real value.

            z (str|int): index or real value.

            wavelength  (str|int): index or real value.

        Returns:
            TaskFile: A general result handler.

        """
        kwargs = dict(x=x, y=y, z=z, wavelength=wavelength)

        return standard_chart(locals())

    @lru_cache(maxsize=None)
    @postmethod
    @bind_monitor_types(TimeMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_td_result_option(
        self, target: str, monitor: Union[int, ProjectComponent]
    ):
        """Get FDTD TD arguments' options.

        Args:
            target (str): The Options: intensity, line.
            monitor (int|MonitorLike): The goal monitor's index or monitor object.

        Returns:
            Dict[str, Any]: Options [key, options]
        """
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fdtd_td_result_option)
    @bind_monitor_types(TimeMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_td_result_chart(
        self,
        target: str,
        monitor: Union[int, ProjectComponent],
        attribute: str,
        operation: str,
        log=False,
        x=0,
        y=0,
        z=0,
        time=0,
    ):
        r"""Get FDTD TD result.

        Args:
            target (str): The Options: intensity, line.

            monitor (int|MonitorLike): The goal monitor's index or monitor object.

            attribute (str): The Options: E, Ex, Ey, Ez, H, Hx, Hy, Hz, Px, Py, Pz, Energy density, T.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            log (bool): Whether to do log operation on data.

            x (str|int): index or real value.

            y (str|int): index or real value.

            z (str|int): index or real value.

            time (str|int): index or real value.

        Returns:
            TaskFile: A general result handler.
        """
        kwargs = dict(x=x, y=y, z=z, time=time)
        return standard_chart(locals())


class V04FDTDSweepResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(
            project,
            targets,
            self.passive_fdtd_sweep_chart,
            self.passive_fdtd_sweep_index_monitor_chart,
        )

    @lru_cache(maxsize=None)
    @postmethod
    @bind_target_selections("line", "intensity")
    def passive_fdtd_sweep_index_monitor_option(self, target: str, monitor):
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fdtd_sweep_index_monitor_option)
    @bind_target_selections("line", "intensity")
    def passive_fdtd_sweep_index_monitor_chart(
        self, target, monitor, attribute, log=False, **kwargs
    ):
        r"""Get FDTD Parameter Sweep result.

        kwargs for sweep dynamic paras.

        Args:

            target (str): The Options: intensity, line.

            monitor

            attribute (str): The Option: "n", "σ".

            log (bool): Whether to do log operation on data.

            \*\*kwargs (): sweep value

        Returns:

        """
        operation = ""
        return standard_chart(locals())

    @lru_cache(maxsize=None)
    @postmethod
    @bind_monitor_types(PowerMonitor, TimeMonitor)
    @bind_target_selections("line", "intensity")
    def passive_fdtd_sweep_result_option_new(
        self, target: str, monitor: Union[int, ProjectComponent]
    ):
        return standard_option(locals())

    passive_fdtd_sweep_option = passive_fdtd_sweep_result_option_new

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fdtd_sweep_option)
    @bind_monitor_types(PowerMonitor, TimeMonitor)
    @bind_target_selections("line", "intensity")
    def passive_fdtd_sweep_result_chart_new(
        self,
        target: str,
        monitor: Union[int, ProjectComponent],
        attribute: str,
        operation: str,
        log=False,
        x=0,
        y=0,
        z=0,
        wavelength=0,
        **kwargs,
    ):
        r"""Get FDTD Parameter Sweep result.

        kwargs for sweep dynamic paras.

        Args:

            target (str): The Options: intensity, line.

            monitor (int|MonitorLike): The goal monitor's index or monitor object.

            attribute (str): The Option: T.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            log (bool): Whether to do log operation on data.

            x (str|int): index or real value.

            y (str|int): index or real value.

            z (str|int): index or real value.

            wavelength  (str|int): index or real value.

            \*\*kwargs (): sweep value

        Returns:

        """
        kwargs.update(x=x, y=y, z=z, wavelength=wavelength)
        return standard_chart(locals())

    passive_fdtd_sweep_chart = passive_fdtd_sweep_result_chart_new


class V04FDTDSmatrixResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(
            project, targets, self.passive_fdtd_smatrix_sweep_chart
        )

    @lru_cache(maxsize=None)
    @postmethod
    # @bind_monitor_types(PowerMonitor, TimeMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_smatrix_sweep_option(self, target: str):
        """Get FDTD SMatrix arguments' options.

        Args:
            target (str): The Options: intensity, line.

        Returns:
            Dict[str, Any]: Options [key, options]
        """
        monitor = 0
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fdtd_smatrix_sweep_option)
    # @bind_monitor_types(PowerMonitor, TimeMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_smatrix_sweep_chart(
        self,
        target: str,
        attribute: str,
        operation: str,
        log=False,
        wavelength=None,
    ):
        r"""Get FDTD SMatrix result.

        Args:
            target (str): The Options: intensity, line.

            attribute (str): The Option: S.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            log (bool): Whether to do log operation on data.

            wavelength (None): You don't have to fill this parameter. The value is controlled automatic inference.

        Returns:
            TaskFile: A general result handler.
        """

        monitor = 0
        if target == "intensity":
            wavelength = 0
        else:
            wavelength = "plotX"

        kwargs = dict(wavelength=wavelength)
        return standard_chart(locals())


class V04FDTDIndexResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(
            project, targets, self.passive_fdtd_index_monitor_chart
        )

    @lru_cache(maxsize=None)
    @postmethod
    @bind_monitor_types(IndexMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_index_monitor_option(
        self, target: str, monitor: Union[int, ProjectComponent]
    ):
        """Get FDTD Index Monitor arguments' options.

        Args:
            target (str): The Options: intensity, line.

        Returns:
            Dict[str, Any]: Options [key, options]
        """
        return standard_option(locals())

    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fdtd_index_monitor_option)
    @bind_monitor_types(IndexMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_index_monitor_chart(
        self,
        target: str,
        monitor: Union[int, ProjectComponent],
        attribute: str,
        log=False,
        **kwargs,
    ):
        r"""Get FDTD Index Monitor result.

        Args:
            target (str): The Options: intensity, line.

            attribute (str): Option are in (n, σ) or (nx, ny, nz, σx, σy, σz). Base on your material selection.

            \*\*kwargs (str): Depends on the plane of monitor

        Returns:
            TaskFile: A general result handler.
        """
        operation = ""
        return standard_chart(locals())


@decohints
def compat_lower(func):
    @wraps(func)
    def wrapper(
        self,
        target: str,
        monitor: Union[int, ProjectComponent],
        attribute: str,
        operation: str,
        log=False,
        mode=0,
        wavelength=0,
    ):
        if attribute.startswith("t_"):
            attribute = "T_" + removeprefix(attribute, "t_")
        if attribute in ["n", "p"]:
            attribute = attribute.upper()

        return func(
            self, target, monitor, attribute, operation, log, mode, wavelength
        )

    return wrapper


class V04ModeExpansionResultHandler(V04API):
    def quick_view(self, project, targets=["intensity", "line", "table"]):
        super().quick_view(
            project, targets, self.passive_fdtd_mode_expansion_chart
        )

    @lru_cache(maxsize=None)
    @postmethod
    @bind_monitor_types(PowerMonitor, TimeMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_mode_expansion_option(
        self, target: str, monitor: Union[int, ProjectComponent]
    ):
        r"""Get FDTD Mode Expansion arguments' options.

        Args:
            target (str): The Options: intensity, line.

            monitor (int|MonitorLike): The goal monitor's index or monitor object.

        Returns:
            Dict[str, Any]: Options [key, options]
        """
        return standard_option(locals())

    @compat_lower
    @parsermethod
    @postmethod
    @coordinate2indexmethod(passive_fdtd_mode_expansion_option)
    @bind_monitor_types(PowerMonitor, TimeMonitor)
    @bind_target_selections("intensity", "line")
    def passive_fdtd_mode_expansion_chart(
        self,
        target: str,
        monitor: Union[int, ProjectComponent],
        attribute: str,
        operation: str,
        log=False,
        mode=0,
        wavelength=0,
    ):
        r"""Get FDTD Mode Expansion result.

        Args:
            target (str): The Options: intensity, line.

            monitor (int|MonitorLike): The goal monitor's index or monitor object.

            attribute (str): The Options: a, b, N, P, T_forward, T_backward.

            operation (str): The Options: ABS, ABS^2, Real, -Real, Imaginary, Angle.

            mode (str|int): index or real value.

            wavelength (str|int): index or real value.

        Returns:
            TaskFile: A general result handler.
        """

        kwargs = dict(mode=mode, wavelength=wavelength)
        return standard_chart(locals())


def options2params(target, options: Dict[str, Any]):
    """Turn options to params

    Args:
        target (str): 'intensity', 'line' and 'table'
        options (dict[str, Any]): data from server.

    Returns:
        Generator[dict[str, str]]: generator of params.

    Doctest
    -------
    >>> ops = {"monitor_x": [1,2,3], "monitor_y": [1.1, 2.2, 3.3], "monitor_z": [-100], "mode": ["1", "2"],
    ...     "attributes": ["E", "P"], "operations": ["ABS"], "dimensions": ["x", "y", "z", "mode"]}
    >>> next(options2params("intensity", ops))
    {'target': 'intensity', 'x': '1', 'y': 'plotX', 'z': '-100', 'mode': 'plotY', 'attribute': 'E', 'operation': 'ABS'}
    >>> # x, y, mode, attributes. Note that swap_axis is disabled
    ... # 16 = 3 * 1 * 1 * 2 + 1 * 1 * 2 * 2 + 1 * 3 * 1 * 2
    ... len(list(options2params("intensity", ops)))
    16


    >>> next(options2params("line", ops))
    {'target': 'line', 'x': '1', 'y': '1.1', 'z': '-100', 'mode': 'plotX', 'attribute': 'E', 'operation': 'ABS'}
    >>> # x, y, mode, attributes
    ... # 42 = 3 * 3 * 1 * 2 + 3 * 1 * 2 * 2 + 1 * 3 * 2 * 2
    ... len(list(options2params("line", ops)))
    42

    >>> next(options2params("table", ops))
    {'target': 'table', 'x': '0', 'y': '0', 'z': '0', 'mode': '0'}
    >>> len(list(options2params("table", ops)))
    1

    """
    if "code" in options:
        options.pop("code")

    ret = {}

    dimensions = options["dimensions"]

    for key in dimensions:
        d_ret = options.get(key) or options.get(f"monitor_{key}")
        assert d_ret
        ret[key] = d_ret

    ret["attribute"] = options.get("attribute") or options.get("attributes")
    ret["operation"] = options.get("operation") or options.get("operations")

    ret_values = list(ret.values())

    names = list(ret.keys())
    if target == "intensity":
        if len(dimensions) > 1:
            dimensions_value = [
                values + ["plotX", "plotY"]
                for _ in dimensions
                if (values := ret[_])
            ]
            dimensions_value = (
                dimensions_value + ret_values[len(dimensions_value) :]
            )
            yield from params_with_target(
                params_filter_for_intensity,
                dimensions,
                dimensions_value,
                names,
                ret,
                target,
            )

    if target == "line":
        if len(dimensions) > 0:
            dimensions_value = [
                values + ["plotX"] for _ in dimensions if (values := ret[_])
            ]
            dimensions_value = (
                dimensions_value + ret_values[len(dimensions_value) :]
            )
            yield from params_with_target(
                params_filter_for_line,
                dimensions,
                dimensions_value,
                names,
                ret,
                target,
            )

    if target == "table":
        dimensions_value = [[0] for _ in dimensions]
        names = names[: len(dimensions_value)]
        yield from params_with_target(
            params_filter_for_table,
            dimensions,
            dimensions_value,
            names,
            ret,
            target,
        )


def params_with_target(
    params_filter_for_, dimensions, dimensions_value, names, ret, target
):
    for params in params_filter_for_(
        ret, params_generator(names, *dimensions_value), dimensions
    ):
        _params = {"target": target}
        _params.update(params)
        yield _params


def params_filter_for_intensity(ret, params_gen, dimensions):
    getter = itemgetter(*dimensions)
    for params in params_gen:
        dimensional_params: List[str] = getter(params)
        if (
            "plotX" in dimensional_params
            and "plotY" in dimensional_params
            and len([_ for _ in dimensional_params if _.startswith("plot")])
            == 2
        ):
            xi = dimensional_params.index("plotX")
            yi = dimensional_params.index("plotY")

            plot_x = dimensions[xi]
            plot_y = dimensions[yi]

            x_lt_y = xi < yi
            x_ok = len(ret[plot_x]) > 1
            y_ok = len(ret[plot_y]) > 1
            if x_lt_y and x_ok and y_ok:
                yield params


def params_filter_for_line(ret, params_gen, dimensions):
    getter = itemgetter(*dimensions)
    for params in params_gen:
        dimensional_params: List[str] = getter(params)
        if (
            "plotX" in dimensional_params
            and len([_ for _ in dimensional_params if _.startswith("plot")])
            == 1
        ):
            xi = dimensional_params.index("plotX")

            plot_x = dimensions[xi]

            x_ok = len(ret[plot_x])
            if x_ok > 1:
                yield params


def params_filter_for_table(ret, params_gen, dimensions):
    yield from params_gen


def params_generator(names, *independents):
    r"""Combinations of independent rows.

    Args:
        names (list[str]): Names of rows.
        \*independents (List[list]): list of possible values.

    Returns:
        Generator(dict[str, Any]): A generator of kwargs.

    Doctest
    -------

    >>> pprint(list(params_generator(['a', 'b', 'c'], [1,2], [1], [100, 1001])))
    [{'a': '1', 'b': '1', 'c': '100'},
     {'a': '1', 'b': '1', 'c': '1001'},
     {'a': '2', 'b': '1', 'c': '100'},
     {'a': '2', 'b': '1', 'c': '1001'}]

    """

    one_row, *independents = independents
    name, *names = names
    is_end = not independents and not names

    for value in one_row:

        if is_end:
            yield {name: str(value)}
        else:
            for dikt in params_generator(names, *independents):
                _dict = {name: str(value)}
                _dict.update(**dikt)
                yield _dict


def params2kwargs(func, *args, **kwargs):
    params = dict(signature(func).parameters)
    params["args"] = Parameter("args", Parameter.VAR_POSITIONAL)
    params["kwargs"] = Parameter("kwargs", Parameter.VAR_KEYWORD)

    oversize_signature = Signature(params.values())

    bounded_arguments = oversize_signature.bind(*args, **kwargs)

    bounded_arguments.apply_defaults()
    bounded_arguments.arguments.popitem(True)
    bounded_arguments.arguments.popitem(True)

    return bounded_arguments
