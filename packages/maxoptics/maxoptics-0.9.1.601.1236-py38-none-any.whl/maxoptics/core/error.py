# coding=utf-8


class PostResultFailedError(Exception):
    pass


class NewConnectionError(Exception):
    pass


class MaxRetryError(Exception):
    pass


class ConnectTimeoutError(Exception):
    pass


class InvalidInputError(Exception):
    pass


class APIError(Exception):
    pass


class SimulationError(Exception):
    pass


class DirtyProjectError(Exception):
    pass


class ProjectBuildError(Exception):
    def __init__(self, component_type, msg):
        msg = "Error found while building {component_type} :\n\t{msg} ".format(
            component_type=component_type, msg=msg
        )
        super(ProjectBuildError, self).__init__(msg)


class ComponentNotFoundError(Exception):
    """
    >>> from maxoptics.var.models import Rectangle
    >>> rec = Rectangle(None)
    >>> rec.name = "123"
    >>> raise ComponentNotFoundError(rec)
    Traceback (most recent call last):
        ...
    error.ComponentNotFoundError: <class 'maxoptics.var.models.MitM.Rectangle'> : `123` not found in current project
    """

    def __init__(self, component):
        msg = "{klass} : `{cname}` not found in current project".format(
            cname=component.name, klass=component.__class__
        )
        super(ComponentNotFoundError, self).__init__(msg)
