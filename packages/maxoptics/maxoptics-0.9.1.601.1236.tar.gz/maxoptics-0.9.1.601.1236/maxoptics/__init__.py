"""This is """
import warnings
from time import sleep

from maxoptics.core.utils import find_maxoptics_conf
from maxoptics.macros import (
    X_Linear,
    Y_Linear,
    Z_Linear,
    Point,
    PortLeftAttach,
    PortRightAttach,
    X_Normal,
    Y_Normal,
    Z_Normal,
)

__all__ = (
    "X_Normal",
    "Y_Normal",
    "Z_Normal",
    "X_Linear",
    "Y_Linear",
    "Z_Linear",
    "Point",
    "PortLeftAttach",
    "PortRightAttach",
    "MosLibrary",
    "__ConfigPath__",
    "__version__",
)

__MainPath__, __ConfigPath__ = find_maxoptics_conf()

# Version Number
__version__ = "0.9.1"


class MosLibrary:
    """Entrance of sdk."""

    def __new__(cls, **kws):
        """Everytime this class is called, config will be reloaded."""

        from maxoptics.config import Config
        from maxoptics.sdk import MaxOptics

        # print("Using Config From", __ConfigPath__)
        if Config.OfflineCompat:
            warnings.warn(
                UserWarning(
                    "You have triggered 'Offline Script Compat Mode' "
                    "and still using MosLibrary() to create new MaxOptics Instance.\n"
                    "The created Instance may not share projects, materials, tasks "
                    "and any operations you have done on other Maxoptics instance(s).\n"
                    "\n"
                    "If you want to access the object and methods hidden by "
                    "writing-style of offline script(s), you can do:\n"
                    "1. `project = solver.__parent_ref__()`, and\n"
                    "2. `client = project.__parent__`\n"
                    "\n"
                    "to access these instances.\n"
                )
            )
            sleep(3)
        Config.__from_MosLibrary__ = True
        mos_instance = MaxOptics()
        Config.__from_MosLibrary__ = False

        if kws:
            mos_instance.config = Config.update(**kws)

        if Config.Login:
            mos_instance.login()

        mos_instance.search_projects()

        Config.__Global_MOS_Instance__ = mos_instance

        return mos_instance
