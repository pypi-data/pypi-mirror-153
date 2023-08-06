from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import arcwaveguide
from maxoptics.var.project import MosProject


class NormalBand(Device):
    def __init__(
        self,
        xy=(0, 0),
        inner_radius=2,
        outer_radius=2.2,
        start_angle=0,
        angle=90,
    ):
        self.xy = xy
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.start_angle = start_angle
        self.angle = angle

    def build(self, p: MosProject, material):
        xy = self.xy
        inner_radius = self.inner_radius
        outer_radius = self.outer_radius
        start_angle = self.start_angle
        angle = self.angle

        SiID = material

        arc = {
            "x": xy[0],
            "y": xy[1],
            "innerRadius": inner_radius,
            "outerRadius": outer_radius,
            "rotate_z": start_angle,
            "angle": angle,
            "materialId": SiID,
        }
        arcwaveguide(p, "arcwaveguide", arc)
        p.save()
        return p
