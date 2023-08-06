from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import (
    rotate_point,
    lineartrapezoid,
    rectangle,
)
from maxoptics.var.project import MosProject


class WgTransition(Device):
    def __init__(
        self,
        xy=(0, 0),
        wg_width=2,
        wg_height=0.22,
        rib_width=4,
        rib_height=0.15,
        taper_length=4,
    ):
        self.xy = xy
        self.wg_width = wg_width
        self.wg_height = wg_height
        self.rib_width = rib_width
        self.rib_height = rib_height
        self.taper_length = taper_length

    def build(self, p: MosProject, material, angle=0):
        xy = self.xy
        wg_width = self.wg_width
        wg_height = self.wg_height
        rib_width = self.rib_width
        rib_height = self.rib_height
        taper_length = self.taper_length

        SiID = material

        rec1_point = rotate_point(
            angle, (xy[0], xy[1], xy[0] - taper_length / 2 - 2, xy[1])
        )
        rec_wg = {
            "x": rec1_point[0],
            "x_span": 4,
            "y": rec1_point[1],
            "y_span": wg_width,
            "z": wg_height / 2,
            "z_span": wg_height,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(p, "waveguide_wg", rec_wg)

        rib_point = rotate_point(angle, (xy[0], xy[1], xy[0], xy[1]))
        taper_rib = {
            "x": rib_point[0],
            "y": rib_point[1],
            "z": (wg_height - rib_height) / 2,
            "z_span": wg_height - rib_height,
            "x0": -wg_width / 2,
            "y0": taper_length / 2,
            "x1": -rib_width / 2,
            "y1": -taper_length / 2,
            "x2": rib_width / 2,
            "y2": -taper_length / 2,
            "x3": wg_width / 2,
            "y3": taper_length / 2,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": 270 + angle,
        }
        lineartrapezoid(p, "taper_rib", taper_rib)

        sub_point = rotate_point(
            angle, (xy[0], xy[1], xy[0] + taper_length / 2 + 2, xy[1])
        )
        rec_sub = {
            "x": sub_point[0],
            "x_span": 4,
            "y": sub_point[1],
            "y_span": rib_width,
            "z": (wg_height - rib_height) / 2,
            "z_span": wg_height - rib_height,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(p, "waveguide_sub", rec_sub)

        rec_rib_point = rotate_point(angle, (xy[0], xy[1], xy[0] + 2, xy[1]))
        rec_rib = {
            "x": rec_rib_point[0],
            "x_span": 4 + taper_length,
            "y": rec_rib_point[1],
            "y_span": wg_width,
            "z": wg_height - rib_height + rib_height / 2,
            "z_span": rib_height,
            "materialId": SiID,
            "meshOrder": 3,
            "rotate_z": angle,
        }
        rectangle(p, "waveguide_rib", rec_rib)
        p.save()

        return p
