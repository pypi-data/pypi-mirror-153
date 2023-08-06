from abc import abstractmethod, ABC

import matplotlib.pyplot as plt

from maxoptics.var.project import MosProject
from maxoptics.core.plot.PolygonLike import compromised_transform


class Device(ABC):
    """_summary_
        @params:
        xy: Device coordinates of the center point
    Args:
        metaclass (_type_, optional): _description_. Defaults to ABCMeta.
    """

    def __init__(self, xy=(0, 0)) -> None:
        self._xy = xy
        self._height = 0.22

    def __str__(self) -> str:
        return str(self.__dict__)

    def visuilize(self, project: MosProject, xysize=(10, 10)):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlim((-xysize[0], xysize[0]))
        ax.set_ylim((-xysize[1], xysize[1]))

        structerList = list(
            filter(
                lambda _: "Project" not in _ and "GlobalMonitor" not in _,
                project.__dict__["components"].keys(),
            )
        )

        for _ in structerList:
            p = project.__dict__["components"][_]
            item = compromised_transform(p)
            ax.add_patch(item.__plot__())
        plt.show()

    @abstractmethod
    def build(self):
        pass
