import dataclasses
import random
import weakref
from math import pi, log, e, sqrt, exp, sin, inf
from typing import Literal

from maxoptics.core.abc import Exportable
from maxoptics.core.logger import error_print


class MaterialPart:
    def __init__(self, material_info, client) -> None:
        self.name = material_info["name"]
        self.id = material_info["id"]
        self.mesh_order = material_info["mesh_order"]
        self.client_weak_ref = weakref.WeakMethod(
            client.get_material_table_data
        )

    @property
    def table_data(self):
        method = self.client_weak_ref()
        if method:
            return method(self.id)["table_data"]
        else:
            error_print("Client was terminated! Can not establish connection.")


@dataclasses.dataclass()
class Material(Exportable):
    name: str
    index_table: dict
    color: str = hex(random.randint(0, 256**3))[2:].upper()
    type: str = "List data"
    mesh_order: int = 2
    temperature: float = 300.0
    dispersionflag: int = 1

    # Don't assign
    conductivity: float = 0
    id: int = 0

    def __post_init__(self):
        if not self.index_table:
            error_print(
                "Error encountered while creating Material instance:"
                " index_table can not be set as empty dict"
            )
            raise ValueError()
        __keys = list(self.index_table.keys())
        for _ in __keys:
            if not isinstance(_, (float, int)):
                error_print(
                    "Error encountered while creating Material instance:"
                    " keys of index_table must be float or int."
                )
                raise ValueError()

        __values = list(self.index_table.values())
        __lengths = set(len(_) for _ in __values)
        if not len(__lengths) == 1:
            error_print(
                "Error encountered while creating Material instance:"
                " length of values of index_table must be consistent"
            )
            raise ValueError()

        __length = tuple(__lengths)[0]

        if __length == 0:
            error_print(
                "Error encountered while creating Material instance:"
                " values of index_table can not be empty"
            )
            raise ValueError()

        elif __length <= 3:
            self._table_name = f"{self.type}_indexes"
            self._table_head = [
                {
                    "name": "Wavelength (\u03bcm)",
                    "type": "wavelength_frequency",
                },
                {"name": "Re (index)", "type": "re"},
                {"name": "Im (index)", "type": "im"},
                {"name": "Conductivity", "type": "conductivity"},
            ]

        elif __length == 27:
            self._table_name = "anisotropy_data"
            self._table_head = [
                {"name": "Wavelength", "type": "wavelength_frequency"},
                {"name": "rexx  ", "type": "rexx"},
                {"name": "imxx  ", "type": "imxx"},
                {"name": "rexy  ", "type": "rexy"},
                {"name": "imxy  ", "type": "imxy"},
                {"name": "rexz  ", "type": "rexz"},
                {"name": "imxz  ", "type": "imxz"},
                {"name": "reyx  ", "type": "reyx"},
                {"name": "imyx  ", "type": "imyx"},
                {"name": "reyy  ", "type": "reyy"},
                {"name": "imyy  ", "type": "imyy"},
                {"name": "reyz  ", "type": "reyz"},
                {"name": "imyz  ", "type": "imyz"},
                {"name": "rezx  ", "type": "rezx"},
                {"name": "imzx  ", "type": "imzx"},
                {"name": "rezy  ", "type": "rezy"},
                {"name": "imzy  ", "type": "imzy"},
                {"name": "rezz  ", "type": "rezz"},
                {"name": "imzz  ", "type": "imzz"},
                {"name": "ConductivityXX  ", "type": "conductivityXX"},
                {"name": "ConductivityXY  ", "type": "conductivityXY"},
                {"name": "ConductivityXZ  ", "type": "conductivityXZ"},
                {"name": "ConductivityYX  ", "type": "conductivityYX"},
                {"name": "ConductivityYY  ", "type": "conductivityYY"},
                {"name": "ConductivityYZ  ", "type": "conductivityYZ"},
                {"name": "ConductivityZX  ", "type": "conductivityZX"},
                {"name": "ConductivityZY  ", "type": "conductivityZY"},
                {"name": "ConductivityZZ  ", "type": "conductivityZZ"},
            ]
        else:
            error_print(
                "Error encountered while creating Material instance:"
                " length of values of index_table can not be " + str(__length)
            )
            raise ValueError()

    def to_dict(self, *args):
        def align_frame(v, k):
            if len(v) == 2:
                v.append(calc_conductivity(v, 0, float(k)))
            if 17 < len(v) < 27:
                v = list(v + [0] * (27 - len(v)))
                for _ in range(9):
                    v[18 + _] = calc_conductivity(v, _ * 2, float(k))
            if len(self._table_head) - len(v) - 1 > 0:
                raise ValueError(
                    f"The Material parameter 'index_table' must be aligned. "
                    f"Expected length of input item is {len(self._table_head)}, "
                    f"but {v} is given, which has length {len(v)}"
                )
            elif (diff_count := len(self._table_head) - len(v) - 1) < 0:
                return list(v) + [0] * diff_count
            else:
                return list(v)

        return {
            "name": self.name,
            "color": self.color,
            "type": self.type,
            "mesh_order": self.mesh_order,
            "temperature": self.temperature,
            "dispersionflag": self.dispersionflag,
            "public": False,
            "id": self.id,
            "data": {},
            "table_data": {
                self._table_name: {
                    "table_head": self._table_head,
                    **{
                        str(k): align_frame(v, k)
                        for k, v in self.index_table.items()
                    },
                }
            },
        }

    def to_dict2(self):
        columns = [_["type"] for _ in self._table_head]
        table_data = []
        for k, v in self.index_table.items():
            if (diff_count := len(columns) - len(v) - 1) > 0:
                values = [str(k * 1000000), *v] + [0] * diff_count
            elif len(columns) - len(v) - 1 < 0:
                raise ValueError(
                    f"The Material parameter 'index_table' must be aligned. "
                    f"Expected length of input item is {len(self._table_head)}, "
                    f"but {v} is given, which has length {len(v)}"
                )
            else:
                values = [str(k * 1000000), *v]

            table_data.append(dict(zip(columns, values)))

        return {
            "name": self.name,
            "color": self.color,
            "type": self.type,
            "mesh_order": self.mesh_order,
            "temperature": self.temperature,
            "dispersionflag": self.dispersionflag,
            "public": False,
            "id": self.id,
            "data": {"conductivity": self.conductivity},
            "tables": {"table_data": table_data},
        }


@dataclasses.dataclass()
class Waveform(Exportable):
    name: str
    para1: float
    para2: float
    input_field: Literal["frequency", "wavelength"] = "frequency"
    input_type: Literal["center_span", "start_stop"] = "center_span"
    id: int = 0
    __offset: float = 21.92

    def __post_init__(self):
        if self.input_field not in ["frequency", "wavelength"]:
            print('Error: input_field must be in ["frequency", "wavelength"]')
            raise ValueError()

        if self.input_type not in ["center_span", "start_stop"]:
            print('Error: input_type must be in ["center_span", "start_stop"]')
            raise ValueError()

    @property
    def data(self):
        return {
            "center_frequency": self.center_frequency,
            "frequency_span": self.frequency_span,
            "center_wavelength": self.center_wavelength,
            "wavelength_span": self.wavelength_span,
            "frequency_start": self.frequency_start,
            "frequency_stop": self.frequency_stop,
            "wavelength_start": self.wavelength_start,
            "wavelength_stop": self.wavelength_stop,
        }

    @staticmethod
    def c(_):
        if _ != 0:
            return 299.792458 / _
        else:
            return inf

    @property
    def state(self):
        return ["frequency", "wavelength"].index(self.input_field) + [
            "center_span",
            "start_stop",
        ].index(self.input_type) * 2

    @property
    def center_frequency(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [a, c(a), (a + b) / 2, (c(a) + c(b)) / 2][self.state]

    @property
    def frequency_span(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [b, c(a - b / 2) - c(a + b / 2), b - a, c(a) - c(b)][self.state]

    @property
    def center_wavelength(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [c(a), a, (c(a) + c(b)) / 2, (a + b) / 2][self.state]

    @property
    def wavelength_span(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [c(a - b / 2) - c(a + b / 2), b, c(a) - c(b), b - a][self.state]

    @property
    def frequency_start(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [a - b / 2, c(a + b / 2), a, c(b)][self.state]

    @property
    def frequency_stop(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [a + b / 2, c(a - b / 2), b, c(a)][self.state]

    @property
    def wavelength_start(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [c(a + b / 2), a - b / 2, c(b), a][self.state]

    @property
    def wavelength_stop(self):
        a = self.para1
        b = self.para2
        c = self.c
        return [c(a - b / 2), a + b / 2, c(a), b][self.state]

    def to_dict(self, *args):
        return {
            "name": self.name,
            "data": {
                "bandwidth": self.bandwidth,
                "offset": self.offset,
                "pulselength": self.pulselength,
                **self.data,
            },
            "public": False,
            "id": self.id,
        }

    @property
    def bandwidth(self):
        return max(self.frequency_span, self.center_frequency / 4)

    @property
    def spread(self):
        return 5 * (pi * self.bandwidth) ** 2 / (3 * log(10, e))

    @property
    def pulselength(self):
        return sqrt(4 * pi / self.spread) * 10**3

    @property
    def offset(self):
        fo = 0.8 * self.pulselength
        ro = self.pulselength
        self.__offset = min(max(fo, self.__offset), ro)
        return self.__offset

    def pulse(self, t, t0=0):
        return exp(4 * pi * (t - t0) ** 2 / self.pulselength**2) * sin(
            2 * pi * self.center_frequency * t
        )


def calc_permitivity(indexes, i):
    index_r = float(indexes[i])
    index_i = float(indexes[i + 1])

    return [index_r**2 - index_i**2, 2 * index_r * index_i]


def calc_conductivity(indexes, i, wav):
    tar_per = calc_permitivity(indexes, i)

    return tar_per[1] * 2 * pi * 299792458 / float(wav) * 8.854187817e-12
