from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import (
    rotate_point,
    rectangle,
    beziercurve,
    arcwaveguide,
)
from maxoptics.var.project import MosProject


class Reflector(Device):
    def __init__(
        self,
        xy=(0, 0),
        wg_width=0.2,
        radius=1,
        bezier1=(0, 0.5),
        bezier2=(1, 0.5),
        bezier3=(1, 2.5),
        bezier4=(2, 2.5),
    ):
        self.xy = xy
        self.wg_width = wg_width
        self.radius = radius
        self.bezier1 = bezier1
        self.bezier2 = bezier2
        self.bezier3 = bezier3
        self.bezier4 = bezier4

    def build(self, reflector: MosProject, material, angle=0):
        xy = self.xy
        wg_width = self.wg_width
        radius = self.radius
        bezier1 = self.bezier1
        bezier2 = self.bezier2
        bezier3 = self.bezier3
        bezier4 = self.bezier4

        SiID = material

        rec1_point = rotate_point(angle, (xy[0], xy[1], -3 + xy[0], xy[1]))
        rec1 = {
            "x": rec1_point[0],
            "x_span": 2,
            "y": rec1_point[1],
            "y_span": 1,
            "z": 0,
            "z_span": 0.22,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(reflector, "Rctangle", rec1)

        rec2_point = rotate_point(angle, (xy[0], xy[1], -1 + xy[0], xy[1]))
        rec2 = {
            "x": rec2_point[0],
            "x_span": 2,
            "y": rec2_point[1],
            "y_span": 2,
            "z": 0,
            "z_span": 0.22,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(reflector, "Rctangle_1", rec2)

        bezier1_point = rotate_point(angle, (xy[0], xy[1], xy[0], xy[1]))
        bezier_1 = {
            "x": bezier1_point[0],
            "y": bezier1_point[1],
            "z": 0,
            "z_span": 0.22,
            "w": wg_width,
            "x0": bezier1[0],
            "y0": bezier1[1],
            "x1": bezier2[0],
            "y1": bezier2[1],
            "x2": bezier3[0],
            "y2": bezier3[1],
            "x3": bezier4[0],
            "y3": bezier4[1],
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        beziercurve(reflector, "Beziercurve", bezier_1)

        bezier2_point = rotate_point(angle, (xy[0], xy[1], xy[0], xy[1]))
        bezier_2 = {
            "x": bezier2_point[0],
            "y": bezier2_point[1],
            "z": 0,
            "z_span": 0.22,
            "w": wg_width,
            "x0": bezier1[0],
            "y0": -bezier1[1],
            "x1": bezier2[0],
            "y1": -bezier2[1],
            "x2": bezier3[0],
            "y2": -bezier3[1],
            "x3": bezier4[0],
            "y3": -bezier4[1],
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        beziercurve(reflector, "Beziercurve_1", bezier_2)

        arc1_point = rotate_point(
            angle, (xy[0], xy[1], 2 + xy[0], xy[1] + bezier3[1] - radius)
        )
        arc1 = {
            "x": arc1_point[0],
            "y": arc1_point[1],
            "z": 0,
            "z_span": 0.22,
            "innerRadius": radius - wg_width / 2,
            "outerRadius": radius + wg_width / 2,
            "angle": 90,
            "rotate_z": 270 + angle,
            "materialId": SiID,
        }
        arcwaveguide(reflector, "ArcWaveguide", arc1)

        arc2_point = rotate_point(
            angle, (xy[0], xy[1], 2 + xy[0], xy[1] - bezier3[1] + radius)
        )
        arc2 = {
            "x": arc2_point[0],
            "y": arc2_point[1],
            "z": 0,
            "z_span": 0.22,
            "innerRadius": radius - wg_width / 2,
            "outerRadius": radius + wg_width / 2,
            "angle": 90,
            "rotate_z": 0 + angle,
            "materialId": SiID,
        }
        arcwaveguide(reflector, "ArcWaveguide_1", arc2)

        rec3_point = rotate_point(
            angle,
            (xy[0], xy[1], xy[0] + bezier3[1] - bezier1[1] + radius, xy[1]),
        )
        rec3 = {
            "x": rec3_point[0],
            "x_span": wg_width,
            "y": rec3_point[1],
            "y_span": (bezier3[1] - radius) * 2,
            "z": 0,
            "z_span": 0.22,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(reflector, "Rctangle_2", rec3)

        reflector.save()

        return reflector
