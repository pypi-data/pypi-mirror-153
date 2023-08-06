from typing import Any

from maxoptics.core.error import InvalidInputError, ComponentNotFoundError
from maxoptics.core.logger import error_print
from maxoptics.core.project.ProjectBase import (
    yield_components_with_type,
)


class Index:
    """Provide unified index counter for monitors and port."""

    def __init__(self, project, task_type, tarsrc_name=None) -> None:
        self.project = project
        self.task_type = task_type
        self.tarsrc_name = tarsrc_name

    def __call__(self, index_info) -> Any:
        from maxoptics.core.component.base.Component import ProjectComponent

        if isinstance(index_info, int):
            return index_info

        elif isinstance(index_info, ProjectComponent):
            # Don't want to import from var (and handle exceptions), use type.name rather than class

            viewer = index_info
            if viewer.type.name == "IndexMonitor":
                for i, (_, component) in enumerate(
                    yield_components_with_type("IndexMonitor", self.project)
                ):
                    if component is viewer:
                        return i

                raise ComponentNotFoundError(viewer)

            elif viewer.type.name == "PowerMonitor":
                if self.task_type == "MODE_EXPANSION":
                    for i, (_, component) in enumerate(
                        yield_components_with_type(
                            "PowerMonitor", self.project
                        )
                    ):
                        if component is viewer:
                            return i

                    raise ComponentNotFoundError(viewer)

                else:
                    for i, (_, component) in enumerate(
                        yield_components_with_type(
                            ("TimeMonitor", "PowerMonitor"), self.project
                        )
                    ):
                        if component is viewer:
                            return i

                    raise ComponentNotFoundError(viewer)

            elif viewer.type.name == "FDTDPort":
                shift = len(
                    list(
                        yield_components_with_type(
                            ("TimeMonitor", "PowerMonitor"), self.project
                        )
                    )
                )

                for i, (_, component) in enumerate(
                    yield_components_with_type("FDTDPort", self.project)
                ):
                    if component is viewer:
                        return i + shift

            elif viewer.type.name == "TimeMonitor":
                for i, (_, component) in enumerate(
                    yield_components_with_type(
                        ("TimeMonitor", "PowerMonitor"), self.project
                    )
                ):
                    if component is viewer:
                        return i

                raise ComponentNotFoundError(viewer)

            elif viewer.type.name == "ProfileMonitor":
                for i, (_, component) in enumerate(
                    yield_components_with_type("ProfileMonitor", self.project)
                ):
                    if component is viewer:
                        return i

                raise ComponentNotFoundError(viewer)

            else:
                for i, (_, component) in enumerate(
                    yield_components_with_type(viewer.type.name, self.project)
                ):
                    if component is viewer:
                        return i

                raise ComponentNotFoundError(viewer)

        else:
            error_print(f"Got an unexpected input: {index_info}")
            raise InvalidInputError()
