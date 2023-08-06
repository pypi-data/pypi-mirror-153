import json
import os
from collections import defaultdict
from itertools import count
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Type, TypeVar, Union

from maxoptics.core.component.base.base import FP, StyleBase
from maxoptics.core.component.base.Component import (
    EmptyComponent,
    Monitor,
    Port,
    PortGroup,
    ProjectComponent,
    Solver,
    Source,
    Structure,
    SweepBase,
)
from maxoptics.core.logger import error_print, info_print
from maxoptics.core.utils import fstr
from maxoptics.core.utils.constraints import pr
from maxoptics.core.utils.currying import fast_currying
from maxoptics.var.config import Config


def ensure_log_folder(log_folder):
    log_folder = Path(log_folder)
    try:
        os.makedirs(log_folder, exist_ok=True)
    except Exception as e:
        error_print(f"Folder {log_folder} doesn't exist, and makedirs failed.")
        raise e
    return log_folder


class ProjectBase(FP):
    def __init__(
        self,
        parent,
        token: str,
        name: str,
        project_type: str,
        log_folder: Optional[Union[str, Path]],
    ):
        self.id: int
        self.version: str
        self.token: str = token

        self.__parent__ = parent
        self.name: str = name
        self.type: str = project_type
        self.components: Dict[str, ProjectComponent] = defaultdict(
            lambda: EmptyComponent()
        )
        self.appendix: Dict[str, Union[ProjectComponent, List]] = {}

        if log_folder is None:
            log_folder = Config.DefaultLogFolderTemplate.format(project=self)

        self.log_folder = ensure_log_folder(log_folder)

    def attach_component(
        self,
        component: ProjectComponent,
        name: str,
    ):
        return attach_component_to_project(component, self=self)

    # TODO
    def format_components(self, container=None, key="data", check=True):
        """
        Format all components in project as a json string

        Args:
            container (dict): other key-value pairs
            key (str): where to be attached

        Returns:

        """

        def panic(maybe_err):
            if isinstance(maybe_err, Exception):
                raise maybe_err
            return maybe_err

        if check:
            pr().emit(self, "ProjectPreSave", None)

        if container is None:
            container = {}

        container[key] = dict(self.appendix)

        return json.dumps(
            container,
            default=lambda o: panic(o.export) if hasattr(o, "export") else {},
        )

    @property
    def ports(self):
        return [_ for n, _ in yield_components_with_class(Port, self)]

    @property
    def monitors(self):
        return [_ for n, _ in yield_components_with_class(Monitor, self)]

    @property
    def sources(self):
        return [_ for n, _ in yield_components_with_class(Source, self)]

    @property
    def sources2(self):
        sources: List[Union[Source, Port]] = list(self.sources)

        if self.port_groups:
            sp = self.port_groups[0].attrs.source_port
            if isinstance(sp, str):
                source_port_id = sp
            elif isinstance(sp, StyleBase):
                source_port_id = sp.id

            port_ids = [_.id for _ in self.ports]
            assert (
                source_port_id in port_ids
            ), f"Goal source monitor not found, monitor id is {source_port_id}"
            index = port_ids.index(source_port_id)
            sources.append(self.ports[index])

        return sources

    @property
    def solver(self):
        return get_component_with_class(Solver, self)[1] or EmptyComponent(
            self
        )

    @property
    def port_groups(self):
        return [_ for n, _ in yield_components_with_class(PortGroup, self)]

    @property
    def polygons(self):
        return [_ for n, _ in yield_components_with_class(Structure, self)]

    @property
    def structures(self):
        return [_ for n, _ in yield_components_with_class(Structure, self)]

    @property
    def sweeps(self):
        return [_ for n, _ in yield_components_with_class(SweepBase, self)]


@fast_currying
def attach_component_to_project(
    component: ProjectComponent, self: ProjectBase
) -> ProjectBase:
    for _type in component.__class__.__mro__:
        pr().emit(self, f"ProjectAdd{_type.__name__}", component)
    attach_component_to_components(self.components, component)
    attach_component_to_parent(component, self)
    return self


def attach_component_to_parent(component, self: ProjectBase):
    belong2 = component.__belong2__
    if self.type not in belong2:
        raise NotImplementedError(
            f"Attaching {component.__class__.__name__} to {self.type} project is not implemented yet."
        )
    parent_components, belong_options = get_parent_components(belong2, self)
    parent = select_parent(parent_components, belong_options, component, self)
    if parent:
        parent.adopt_component(component)


def select_parent(
    available_comps, belong_options, component, self: ProjectBase
):
    if "$" in available_comps:
        root_pointer = belong_options[0]

        root_key = fstr(root_pointer).removeprefix("$<----")
        if root_key.endswith("*"):
            root_key = str(root_key.removesuffix("*"))
            old: List = self.appendix.get(root_key, [])
            assert isinstance(
                old, list
            ), f"Attribute {root_key} got value {old}"

            self.appendix[root_key] = old + [component]
        else:
            root_key = str(root_key)
            self.appendix[root_key] = component

        return None
    elif not available_comps:
        raise IndexError(
            f"Cannot find prerequisite component with type {belong_options} "
            f"for incoming component {component.name}"
        )

    elif (length := len(available_comps)) > 1:
        info_print(
            f"There are {length} available component for {component.name} to attach:"
        )
        for i, comp in enumerate(available_comps):
            info_print(f"{i + 1}. {comp.__class__.__name__}: {comp.name}")

        print("\n")
        select = int(input("Which you want to choose (input number):"))
        return available_comps[select]
    else:
        return available_comps[0]


def get_parent_components(belong2, self):
    belong_options: List[str] = belong2[self.type]
    parent_components: List[ProjectComponent] = []
    for option in belong_options:
        if option in ["*"]:
            continue
        elif "$" in option:  # No need to attach
            parent_components = ["$"]
        else:
            for par_component in self.components.values():
                if par_component.__class__.__name__ == option:
                    parent_components.append(par_component)
    return parent_components, belong_options


c = defaultdict(lambda: count(2))
# c = defaultdict(count)


def attach_component_to_components(components, component):
    """Let project.components contains the new component.

    Args:
        components (dict[str, ProjectComponent]): project.components
        component (ProjectComponent): The new component

    Returns:
        None
    """
    name = component.name

    if name in components:
        # warn_print(
        #     f"You creates {name} as\n"
        #     f"{component}\n"
        #     f", but the \n"
        #     f"{name}:{components[name].__dataclass__repr__({'attrs': '*'}, extract_all=False)}\n"
        #     f"exists."
        # )
        name = component.name = f"{name}_auto_count_{next(c[name])}"

    components[name] = component


def yield_components_with_type(
    type_name: Union[str, Tuple[str]], project: ProjectBase
) -> Generator[Tuple[str, ProjectComponent], None, None]:
    components = project.components
    for name, component in list(components.items()):
        if isinstance(type_name, str):
            if component.type.name == type_name:
                if component.disabled is False:
                    yield name, component

        elif isinstance(type_name, tuple):
            if component.type.name in type_name:
                if component.disabled is False:
                    yield name, component

        else:
            raise ValueError("Expect type_name as str or list[str]")


def get_component_with_type(
    type_name: Union[str, Tuple[str]], project: ProjectBase
) -> Tuple[str, ProjectComponent]:
    try:
        iterable = yield_components_with_type(type_name, project)
        name, component = next(iterable)
    except StopIteration:
        name, component = "", None
    finally:
        iterable.close()

    return name, component


T = TypeVar("T")  # ProjectComponent


def yield_components_with_class(
    cls: Type[T], project: ProjectBase
) -> Generator[Tuple[str, T], None, None]:
    components = project.components
    for name, component in list(components.items()):
        if isinstance(component, cls):
            if component.disabled is False:
                yield name, component


def get_component_with_class(
    cls: Type[T], project: ProjectBase
) -> Tuple[str, T]:
    try:
        iterable = yield_components_with_class(cls, project)
        name, component = next(iterable)
    except StopIteration:
        name, component = "", None
    finally:
        iterable.close()

    return name, component
