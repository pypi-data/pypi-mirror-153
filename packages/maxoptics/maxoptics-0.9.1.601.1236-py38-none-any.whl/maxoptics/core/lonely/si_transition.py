from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import (
    rotate_point,
    rectangle,
    lineartrapezoid,
)
from maxoptics.var.project import MosProject
from maxoptics.sdk import MaxOptics


class SiTransition(Device):
    def __init__(
        self,
        xy=(0, 0),
        Si_width=0.5,
        Si_height=0.22,
        Si_taper_width=0.08,
        Si_taper_length=10,
        SiN_width=1,
        SiN_height=0.3,
        SiN_taper_width=0.5,
        SiN_taper_length=10,
        gap=0.08,
    ):
        self.xy = xy
        self.Si_width = Si_width
        self.Si_height = Si_height
        self.SiN_width = SiN_width
        self.SiN_height = SiN_height
        self.Si_taper_width = Si_taper_width
        self.SiN_taper_width = SiN_taper_width
        self.Si_taper_length = Si_taper_length
        self.SiN_taper_length = SiN_taper_length
        self.gap = gap

    def build(self, p: MosProject, angle=0):
        xy = self.xy
        Si_width = self.Si_width
        Si_height = self.Si_height
        SiN_width = self.SiN_width
        SiN_height = self.SiN_height
        Si_taper_width = self.Si_taper_width
        SiN_taper_width = self.SiN_taper_width
        Si_taper_length = self.Si_taper_length
        SiN_taper_length = self.SiN_taper_length
        gap = self.gap

        client = MaxOptics()
        SiID = client.public_materials["Si (Silicon) - Palik"]["id"]
        SiNID = client.public_materials["Si3N4 (Silicon Nitride) - Kischkat"][
            "id"
        ]

        Si_point = rotate_point(
            angle, (xy[0], xy[1], xy[0] - Si_taper_length / 2 - 2.5, xy[1])
        )
        rec_Si = {
            "x": Si_point[0],
            "x_span": 5,
            "y": Si_point[1],
            "y_span": Si_width,
            "z": 0.11,
            "z_span": Si_height,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(p, "waveguide_Si", rec_Si)

        SiN_point = rotate_point(
            angle, (xy[0], xy[1], xy[0] + SiN_taper_length / 2 + 2.5, xy[1])
        )
        rec_SiN = {
            "x": SiN_point[0],
            "x_span": 5,
            "y": SiN_point[1],
            "y_span": SiN_width,
            "z": 0.11 + Si_height / 2 + SiN_height / 2 + gap,
            "z_span": SiN_height,
            "materialId": SiNID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(p, "waveguide_SiN", rec_SiN)

        taper_Si_point = rotate_point(angle, (xy[0], xy[1], xy[0], xy[1]))
        taper_Si = {
            "x": taper_Si_point[0],
            "y": taper_Si_point[1],
            "z": 0.11,
            "z_span": Si_height,
            "x0": -Si_taper_length / 2,
            "y0": Si_width / 2,
            "x1": -Si_taper_length / 2,
            "y1": -Si_width / 2,
            "x2": Si_taper_length / 2,
            "y2": -Si_taper_width / 2,
            "x3": Si_taper_length / 2,
            "y3": Si_taper_width / 2,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        lineartrapezoid(p, "taper_Si", taper_Si)

        taper_SiN_point = rotate_point(angle, (xy[0], xy[1], xy[0], xy[1]))
        taper_SiN = {
            "x": taper_SiN_point[0],
            "y": taper_SiN_point[1],
            "z": 0.11 + Si_height / 2 + SiN_height / 2 + gap,
            "z_span": SiN_height,
            "x0": -SiN_taper_length / 2,
            "y0": SiN_taper_width / 2,
            "x1": -SiN_taper_length / 2,
            "y1": -SiN_taper_width / 2,
            "x2": SiN_taper_length / 2,
            "y2": -SiN_width / 2,
            "x3": SiN_taper_length / 2,
            "y3": SiN_width / 2,
            "materialId": SiNID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        lineartrapezoid(p, "taper_SiN", taper_SiN)

        p.save()
        return p
