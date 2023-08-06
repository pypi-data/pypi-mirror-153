from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from maxoptics.core.utils import ShadowAttr
from maxoptics.core.visualizer.utils import parsermethod, postmethod
from maxoptics.var.MosIO import WhaleClients


class V03API(WhaleClients):
    api_version = "0.3"

    def fields(self):
        """NotImplemented"""

    def dump_all(self):
        """NotImplemented"""

    def sync_download(self):
        """NotImplemented"""


class V03EMEResultHandler(V03API):
    @parsermethod
    def get_smatrix(self, task_type, target="intensity"):
        res = self.post(taskid=int(self.task_id), type=task_type)
        assert res.get("success")
        result = res["result"]
        n = result["n"]
        data = np.reshape(result["data"], (n, n))
        return {
            "data": data,
            "dWidth": list(range(1, n + 1)),
            "dHeight": list(range(1, n + 1)),
        }

    @parsermethod
    def get_eme_result(
        self, monitor: int, field: str, _type, target="intensity"
    ):
        res = self.post(
            taskid=self.task_id,
            monitor=self.Index(monitor),
            field=field,
            type=_type,
        )
        assert res.get("success")
        result = res["result"]
        nx, ny, ix, iy = 0, 0, 0, 0
        for i, _n in enumerate(result["n"]):
            if _n > 1:
                if not nx:
                    nx = _n
                    ix = i
                else:
                    ny = _n
                    iy = i
        dWidth = result["grid"][f"axis{ix}"]
        dHeight = result["grid"][f"axis{iy}"]
        data = np.reshape(result["data"], (nx, ny))

        return {
            "data": np.transpose(data),
            "dWidth": dWidth,
            "dHeight": dHeight,
        }

    @parsermethod
    def get_eme_sweep_result(self, target="line"):
        res = self.post(taskid=self.task_id)
        assert res.get("success")
        result = res["result"]
        _smatrixs = result["smatrixs"]
        sweep_spans = result["sweep_spans"]

        def possibles(_):
            return np.reshape(
                [
                    [
                        [(is_imag, port2, port1) for is_imag in range(2)]
                        for port2 in range(_["n"])
                    ]
                    for port1 in range(_["n"])
                ],
                (-1, 3),
            )

        smatrixs = map(
            lambda _: [
                _["smatrix"][port1][port2][is_imag]
                for is_imag, port2, port1 in possibles(_)
            ],
            _smatrixs,
        )
        if _smatrixs:
            legend = [
                f'{port1 + 1}_{port2 + 1}_{["real", "imag"][is_imag]}'
                for is_imag, port2, port1 in possibles(_smatrixs[0])
            ]
        else:
            legend = []
        return {
            "data": np.transpose(list(smatrixs)),
            "legend": legend,
            "horizontal": sweep_spans,
        }


class V03PDResultHandler(V03API):
    heatmap = ShadowAttr("_heatmap")

    photon_current = ShadowAttr("_polylines", "photon_current")
    responsivity = ShadowAttr("_polylines", "responsivity")

    potential = ShadowAttr("_dfs", "potential")
    e_conc = ShadowAttr("_dfs", "e_conc")
    h_conc = ShadowAttr("_dfs", "h_conc")
    jx = ShadowAttr("_dfs", "jx")
    jy = ShadowAttr("_dfs", "jy")

    resistance = ShadowAttr("_get_resistance")

    def __init__(self, task_id: int, task_type: str, token: str):
        super().__init__(task_id, task_type)
        self._get_resistance = None
        self._heatmap = None
        self._polylines = None
        self._dfs = None
        self.update_status()
        if self.status == 2:
            self.load_data()

    def load_data(self):
        with self.get_pd_power_result() as data:
            self._dfs = {
                _: pd.DataFrame(
                    np.array(data[_]),
                    columns=data["x"],
                    index=data["y"],
                ).astype(float)
                for _ in ["potential", "e_conc", "h_conc", "jx", "jy"]
            }

        with self.get_gen_rate_heatmap() as data:
            self._heatmap = pd.DataFrame(
                np.array(data["g_r"]),
                columns=data["x_r"],
                index=data["y_r"],
            ).astype(float)

        with self.get_pd_td_polyline() as data:
            self._polylines = {
                _: pd.DataFrame(
                    np.array(data[_]), columns=[_], index=data["t"]
                ).astype(float)
                for _ in ["photon_current", "responsivity"]
            }

        with self.get_resistance() as result:
            self._get_resistance = pd.DataFrame(result, index=[0])

    @contextmanager
    def get_pd_power_result(self, target="intensity"):
        res = self.post(taskid=self.task_id)
        try:
            assert res.get("success")
            yield res["result"]["data"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res

    @contextmanager
    def get_pd_td_polyline(self, target="line"):
        res = self.post(taskid=self.task_id)
        try:
            assert res.get("success")
            yield res["result"]["data"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res

    @contextmanager
    def get_resistance(self, target="intensity"):
        res = self.post(taskid=self.task_id)
        try:
            assert res.get("success")
            yield res["result"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res

    @contextmanager
    def get_gen_rate_heatmap(self, target="intensity"):
        res = self.post(taskid=self.task_id)
        try:
            assert res.get("success")
            yield res["result"]["data"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res

    @contextmanager
    def get_fdtd_grid(self, monitor: int, target="intensity"):
        res = self.post(
            taskid=self.task_id,
            monitor_index=monitor,
        )
        try:
            assert res.get("success")
            yield res["result"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res

    @contextmanager
    def get_fdtd_fd_result(
        self,
        monitor: int,
        frequency_index: int,
        field: str,
        _type: str,
        target="intensity",
    ):
        res = self.post(
            taskid=self.task_id,
            monitor_index=monitor,
            freq_index=frequency_index,
            field=field,
            type=_type,
        )
        try:
            assert res.get("success")
            yield res["result"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res


class V03ModulatorResultHandler(V03API):
    potential = ShadowAttr("_dfs", "potential")
    e_conc = ShadowAttr("_dfs", "e_conc")
    h_conc = ShadowAttr("_dfs", "h_conc")
    jx = ShadowAttr("_dfs", "jx")
    jy = ShadowAttr("_dfs", "jy")
    dk = ShadowAttr("_dfs", "dk")
    dn = ShadowAttr("_dfs", "dn")

    resistance = ShadowAttr("_get_resistance")

    def __init__(self, task_id: int, task_type: str, token: str):
        super().__init__(task_id, task_type)
        self._dfs = None
        self._get_resistance = None
        self.update_status()
        if self.status == 2:
            self.load_data()

    def load_data(self):
        with self.get_resistance() as result:
            self._get_resistance = pd.DataFrame(result, index=[0])

        with self.get_modulator_result() as result:
            self._dfs = {
                _: pd.DataFrame(
                    np.array(result[_]),
                    columns=result["x"],
                    index=result["y"],
                ).astype(float)
                for _ in [
                    "potential",
                    "e_conc",
                    "h_conc",
                    "jx",
                    "jy",
                    "dk",
                    "dn",
                ]
            }

    @contextmanager
    def get_modulator_result(self, target="intensity"):
        res = self.post(taskid=self.task_id)
        try:
            assert res.get("success")
            yield res["result"]["data"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res

    @contextmanager
    def get_resistance(self, target="table"):
        res = self.post(taskid=self.task_id)
        try:
            assert res.get("success")
            yield res["result"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res

    @contextmanager
    def get_mode_solver_result(
        self,
        mode_index: int,
        field: str,
        _type: str,
        log: bool = False,
        target: str = "intensity",
    ):
        res = self.post(
            taskid=self.task_id,
            option=dict(
                mode_index=mode_index, field=field, type=_type, log=log
            ),
        )
        try:
            assert res.get("success")
            yield res["result"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res


class V03ModeExpansionResultHandler(V03API):
    @contextmanager
    def get_mode_expansion(self, target="line"):
        res = self.post(taskid=self.task_id)
        try:
            assert res.get("success")
            yield res["result"]
        except AssertionError:
            print("Fetch result failed")
        finally:
            del res


def add0(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        diff = ret["horizontal"][1] - ret["horizontal"][1]
        ret["horizontal"] = (
            [0] + ret["horizontal"] + [ret["horizontal"][-1] + diff]
        )
        diff = ret["vertical"][1] - ret["vertical"][1]
        ret["vertical"] = [0] + ret["vertical"] + [ret["vertical"][-1] + diff]
        return ret


class V03UserImport(V03API):
    def __init__(self, config):
        super().__init__(-1, None, config)

    def upload_files(self, file: str):
        file_name = Path(file).name
        token = self.token
        files = [
            (
                "files",
                (
                    file_name,
                    open(Path(file), "rb"),
                    "application/octet-stream",
                ),
            )
        ]
        res = requests.request(
            "POST",
            self.api_url % "upload_files",
            headers={},  # {"Content-Type": "multipart/form-data;boundary=--"}
            data={"token": token},
            files=files,
        )
        return res.text

    def get_user_mode_files(self):
        ret = self.post(url="get_user_mode_files")
        assert ret["success"]
        data = ret["result"]["data"]
        return data

    @add0
    @postmethod
    def get_user_mode_file_options(self, file_name):
        return {"file_name": file_name}

    @add0
    @postmethod
    def get_user_mode_file_chart(
        self, target, file_name, attribute, operation
    ):
        return {
            "file_name": file_name,
            "pub": {"attribute": attribute, "operation": operation},
        }
