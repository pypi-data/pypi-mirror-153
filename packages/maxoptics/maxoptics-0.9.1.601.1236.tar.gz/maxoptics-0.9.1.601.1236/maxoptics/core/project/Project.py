from typing import Any, List, Dict, Union

from maxoptics.core.component.base.Component import ProjectComponent
from maxoptics.core.error import InvalidInputError
from maxoptics.core.gdstools import GdsParser
from maxoptics.core.logger import (
    error_print,
)
from maxoptics.core.project.ProjectBase import (
    ProjectBase,
)
from maxoptics.core.utils import camel_to_snake


class ProjectCore(ProjectBase):
    """
    Project Class, for basic structure/simulation addition, project configuration and so on
    """

    def __init__(
        self,
        parent,
        token,
        name=None,
        project_type=None,
        log_folder=None,
    ):
        if name is None:
            name = "Any"
        if project_type is None:
            project_type = "passive"

        super(ProjectCore, self).__init__(
            parent, token, name, project_type, log_folder
        )
        # Overwrite
        self.appendix: Dict[str, Union[Dict, List]] = {
            "history": {},
            "result": {},
        }
        self.id = 0
        self.solver_name: str = ""
        self.solver_type: str = ""
        self.tasks: List[dict] = []
        self.running_tasks: List[Any] = []

    def resize(self, w=None, h=None, dx=None, dy=None):
        """Soon will expire.
        Resize the canvas of project.
        You can write those attributes directly into `DOCUMENT` of project now,
        so you should never use this method.
        """

        class VerificationError(Exception):
            def __init__(self, msg="", code=0):
                self.msg = msg
                self.code = code

        def verify(num):
            if num is None:
                return
            if num < 0:
                raise VerificationError(msg="Input cannot be negative!")
            if num == 0:
                raise VerificationError(msg="Input cannot be zero!")
            # More
            return num

        try:
            if verify(w):
                self.DOCUMENT["attrs"]["w"] = w
            if verify(h):
                self.DOCUMENT["attrs"]["h"] = h
            if verify(dx):
                self.DOCUMENT["attrs"]["drawGrid"]["dx"] = dx
            if verify(dy):
                self.DOCUMENT["attrs"]["drawGrid"]["dy"] = dy
        except VerificationError as e:
            error_print(e.msg)
            return
        return

    def add(self, class_name, name="") -> ProjectComponent:
        """Add a component to this project.
        Where this component will be attached will be determined by its `belong2` attribute.
        Most of the components will be attached to `DOCUMENT` component, which is created with project simultaneously`

        Args:
            class_name (str): The type of the component.

            name (str, optional): The name of the component. Defaults to "".

        Returns:
            The added component.
        """
        ret = dynamic_add(class_name, name, self)
        return ret

    def getItemByName(self, name):
        """ """
        res = self.components[name]
        if res is None:
            import traceback

            error_print("No component with name", name)
            traceback.print_exc()
            raise InvalidInputError
        return res

    def __getitem__(self, name: str):
        return self.getItemByName(name)

    def __setitem__(self, name: str, value: Any):
        self.components[name] = value

    def export(self, name: str = None, _format="json"):
        self.__parent__.export_project(self, name, _format=_format)

    def save(self, check=True):
        return self.__parent__.save_project(self, check=check)

    def gds_import(self, gdsfile, cellname, layer, material, zmin, zmax):
        model = GdsParser.GdsModel(self, self.__parent__)
        return model.gds_import(gdsfile, cellname, layer, material, zmin, zmax)

    def add_polygon(self, points):
        model = GdsParser.GdsModel(self, self.__parent__)
        return model.gen_polygon(points)


"""Utils"""


def dynamic_add(class_name, name, self: ProjectCore):
    method_name = "???"
    method_name = camel_to_snake("create" + class_name).strip()
    method = getattr(self, method_name)
    if name:
        ret = method(name=name)
    else:
        ret = method()

    return ret
