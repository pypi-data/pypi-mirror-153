"""The BaseContainer module defines classes to represent materials and waveforms,
and base class of Material/Waveform searcher.
"""
from copy import deepcopy
from math import nan
from typing import TypeVar, List, Optional, Generic

from maxoptics.core.base import Material
from maxoptics.core.abc import Exportable
from maxoptics.core.base import Waveform
from maxoptics.core.logger import error_print


class XXShell(Exportable):
    """Initialization for material and waveform.
    Instances turn into their id when project is parsed by
    `json.dump(..., default=lambda o: o.export if hasattr(o, "export") else {})`.
    Can also be evaluated as dict.
    """

    def __init__(self, raw):
        self.__raw__ = raw
        self.__initialized__ = False

    def __getitem__(self, key):
        """Provide dict-form access.
        Which means `Material0["id"]` writing still works.

        Args:
            key (str): The key.

        Returns:
            Any: The value in raw dict.
        """
        return self.__raw__[key]

    def __getattr__(self, item):
        if not self.__initialized__:
            self.__poi__()

        return super().__getattribute__(item)

    def __poi__(self):
        """Post init. The symbol `__post_init__` may be occupied.

        Returns:
            None
        """
        raise NotImplementedError()

    @property
    def export(self):
        """What to show.

        Returns:
            str|int: The id.
        """
        return self.__getattr__("id")

    def reflected(self, *args, **kwargs):
        return super(XXShell, self).reflected(deepcopy(self.__raw__))


class MaterialShell(XXShell, Material):
    """XXShell for Material."""

    def __init__(self, raw):
        super(MaterialShell, self).__init__(raw)
        # Not working normally when calling `xx.id`, therefore post_init is forced to run
        self.__poi__()

    def __poi__(self):
        """Fill data in `raw` to `Material` form arrange.

        Returns:
            None
        """
        Material.__init__(self, "", {0.01: [nan, nan, nan]})
        r = self.__raw__
        self.id = r["id"]
        self.name = r["name"]
        self.color = r["color"]
        self.type = r["type"]
        self.mesh_order = r["mesh_order"]
        self.temperature = r.get("temperature", 300)

    @property
    def data(self):
        return self.__raw__

    # @property
    # def table_data(self):
    #     """Get the table data of the material.
    #
    #     Returns:
    #         dict: All index, conductivity and wavelength information in this dict.
    #     """
    #     def gmtd_method(material_id):
    #         from maxoptics.var.config import Config
    #         params = {"token": Config.token, "material_id": material_id}
    #         result = self.post(url="get_material_table_data", **params)
    #         if result["success"] is False:
    #             error_print(
    #                 "Material table data fetching failed, %s"
    #                 % result["result"]["msg"]
    #             )
    #         else:
    #             return result["result"]
    #
    #     if gmtd_method:
    #         return gmtd_method(self.id)["table_data"]
    #     else:
    #         error_print(
    #             "Client may be terminated! Failed to establish connection."
    #         )


class WaveformShell(XXShell, Waveform):
    """XXShell for Waveform.

    >>> w1 = WaveformShell({"center_frequency": 1000, "frequency_span": 10, "id": 1111})
    >>> w1['id']
    1111
    >>> w1.export
    1111
    """

    def __init__(self, raw):
        super(WaveformShell, self).__init__(raw)
        # Not working normally when calling `xx.id`, therefore post_init is forced to run
        self.__poi__()

    def __poi__(self):
        """Fill data in `raw` to `Waveform` form arrange.

        Returns:
            None
        """
        Waveform.__init__(self, "", 0, 0)
        r = self.__raw__
        data = self.__raw__["data"]
        self.name = r.get("name", "Unnamed")
        if "center_wavelength" in data and "wavelength_span" in data:
            self.para1 = data["center_wavelength"]
            self.para2 = data["wavelength_span"]
            self.input_field = "wavelength"
            self.input_type = "center_span"
        elif "wavelength_start" in data and "wavelength_stop" in data:
            self.para1 = data["wavelength_start"]
            self.para2 = data["wavelength_stop"]
            self.input_field = "wavelength"
            self.input_type = "start_stop"
        elif "center_frequency" in data and "frequency_span" in data:
            self.para1 = data["center_frequency"]
            self.para2 = data["frequency_span"]
            self.input_field = "frequency"
            self.input_type = "center_span"
        elif "frequency_start" in data and "frequency_stop" in data:
            self.para1 = data["frequency_start"]
            self.para2 = data["frequency_stop"]
            self.input_field = "frequency"
            self.input_type = "start_stop"
        else:
            raise ValueError(f"Income data is invalid: {data = }")

        self.id = r["id"]


T = TypeVar("T")


class BaseSearchContainer(Generic[T]):
    """The BaseSearchContainer implements common methods and properties in Material
    nad Waveform searcher.
    """

    def __init__(self):
        self._cached: Optional[List[T]] = None
        self._faked: Optional[List[T]] = []

    @property
    def names(self):
        """All name as a list.

        Returns:
            list[str]: list of name.
        """
        return list(map(lambda _: _["name"], list(self.all())))

    @property
    def ids(self):
        """All id in a list.

        Returns:
            list[str]: list of id.
        """
        return list(map(lambda _: _["id"], list(self.all())))

    def _get_index(self, keyval: str):
        """Get item with name.

        Returns:
            int: The index of the key.
        """
        names = list(map(lambda _: _["name"], list(self.all())))

        def __get_index(_names, _keyval):
            for i, v in enumerate(_names):
                if _keyval == v:
                    yield i

        indexes = list(__get_index(_names=names, _keyval=keyval))
        if len(indexes) == 0:
            # Not Found
            print(
                f"The {keyval} is not found, please select from one of these:"
            )
            for name in names:
                print("\t", name)
            raise KeyError
        elif len(indexes) == 1:
            return indexes[0]
        else:
            num = len(indexes)
            error_print(f"You got {num} material with same name {keyval}")
            while True:
                answer = input("Delete all of them?(y/n):\n").strip()
                if answer in ["y", "Y"]:
                    deleter = self.deleter()
                    for ind in indexes:
                        deleter(self.all()[ind]["id"])
                    print("\nDeleted. Please rerun.")
                    break
                elif answer in ["n", "N"]:
                    print("\nCanceled. Please check materials before rerun.")
                    break
                else:
                    print("\nPlease input 'y' or 'n'.")
            exit(1)

    # @abstractmethod
    # def deleter(self):
    #     ...

    def all(self):
        """Safely return all contents. Reload from server if contents are empty.

        Returns:
            list[T]: All contents
        """
        if not self._cached:
            self.reload()

        return self._cached + self._faked

    def reload(self):
        """Implemented in subclass."""
        NotImplemented
