"""Under Developing"""
import inspect
from typing import List

from maxoptics.core.component.base.Component import ProjectComponent
from maxoptics.var.project import MosProject
from maxoptics.sdk import MaxOptics


class PCell(MaxOptics):
    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self._methods = inspect.getmembers(
            self,
            lambda _: inspect.ismethod(_)
            and (_.__name__ not in dir(__class__)),
        )
        self._layouts = inspect.getmembers(
            self,
            lambda _: isinstance(_, LayoutView)
            and (_.__name__ not in dir(__class__)),
        )
        print(self._methods, self._layouts)

    class Layout:
        ...


class LayoutView(MosProject):
    def __init__(self, parent, token, name="Any", project_type="passive"):
        super().__init__(parent, token, name, project_type)
        self.name = self.__class__.__name__


class OpticalPort:
    def __new__(cls: type, x_y, angle) -> ProjectComponent:
        # port = EmePort(), x_y, angle
        # attach_port(port)
        # return port
        ...


# Test
if __name__ == "__main__":

    class MyCell(PCell):
        @staticmethod
        def _add_port(ports: List):
            ports.append(OpticalPort((1, 2), 90))
            return ports

        class Layout(LayoutView):
            ...
