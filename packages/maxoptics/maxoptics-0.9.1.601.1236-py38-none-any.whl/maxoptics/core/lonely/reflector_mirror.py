from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.reflector import Reflector
from maxoptics.var.project import MosProject


class ReflectorMirror(Device):
    def __init__(
        self,
        xy=(0, 0),
        gap=1,
        wg_width=0.2,
        radius=1,
        bezier1=(0, 0.5),
        bezier2=(1, 0.5),
        bezier3=(1, 2.5),
        bezier4=(2, 2.5),
    ):
        self.gap = gap
        self.xy = xy
        self.wg_width = wg_width
        self.radius = radius
        self.bezier1 = bezier1
        self.bezier2 = bezier2
        self.bezier3 = bezier3
        self.bezier4 = bezier4

    def build(self, mirror: MosProject, material, angle=0):
        gap = self.gap
        xy = self.xy
        wg_width = self.wg_width
        radius = self.radius
        bezier1 = self.bezier1
        bezier2 = self.bezier2
        bezier3 = self.bezier3
        bezier4 = self.bezier4

        SiID = material
        mirror_left = Reflector(
            xy=(xy[0] - 3 - gap / 2 - wg_width / 2, xy[1]),
            radius=radius,
            bezier1=bezier1,
            bezier2=bezier2,
            bezier3=bezier3,
            bezier4=bezier4,
        )
        mirror_left.build(mirror, SiID, angle)
        mirror_right = Reflector(
            xy=(xy[0] + 3 + gap / 2 + wg_width / 2, xy[1]),
            radius=radius,
            bezier1=bezier1,
            bezier2=bezier2,
            bezier3=bezier3,
            bezier4=bezier4,
        )
        mirror_right.build(mirror, SiID, angle=angle + 180)
