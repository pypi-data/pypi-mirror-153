from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import (
    rectangle,
    lineartrapezoid,
    rotate_point,
)
from maxoptics.var.project import MosProject


class Cross(Device):
    def __init__(
        self,
        xy=(0, 0),
        taper_length=2,
        taper_width=0.8,
        wg_width=0.5,
        mmi_length=4,
    ) -> None:
        super().__init__(xy)
        self._taper_length = taper_length
        self._taper_width = taper_width
        self._wg_width = wg_width
        self._mmi_length = mmi_length

    def build(self, cross: MosProject, material, angle=0):
        SiID = material
        vmmi_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "x_span": self._mmi_length,
            "y_span": self._taper_width,
            "z_span": self._height,
            "materialId": SiID,
            "meshOrder": 2,
            "rotate_z": angle,
        }
        rectangle(cross, "verticalMmi", vmmi_attrs)

        hmmi_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "x_span": self._taper_width,
            "y_span": self._mmi_length,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(cross, "horizontalMmi", hmmi_attrs)

        rT_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": self._mmi_length / 2,
            "y0": self._taper_width / 2,
            "x1": self._mmi_length / 2,
            "y1": -self._taper_width / 2,
            "x2": self._mmi_length / 2 + self._taper_length,
            "y2": -self._wg_width / 2,
            "x3": self._mmi_length / 2 + self._taper_length,
            "y3": self._wg_width / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        lineartrapezoid(cross, "rightTaper", rT_attrs)

        rw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._mmi_length / 2
                + self._taper_length * 3 / 2
                + self._xy[0],
                self._xy[1],
            ),
        )
        rW_attrs = {
            "x": rw_point[0],
            "y": rw_point[1],
            "x_span": self._taper_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(cross, "rightWg", rW_attrs)

        lT_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": -self._mmi_length / 2,
            "y0": self._taper_width / 2,
            "x1": -self._mmi_length / 2,
            "y1": -self._taper_width / 2,
            "x2": -(self._mmi_length / 2 + self._taper_length),
            "y2": -self._wg_width / 2,
            "x3": -(self._mmi_length / 2 + self._taper_length),
            "y3": self._wg_width / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        lineartrapezoid(cross, "leftTaper", lT_attrs)

        lw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                -(self._mmi_length / 2 + self._taper_length * 3 / 2)
                + self._xy[0],
                self._xy[1],
            ),
        )
        lw_attrs = {
            "x": lw_point[0],
            "y": lw_point[1],
            "x_span": self._taper_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(cross, "leftWg", lw_attrs)

        uT_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": -self._taper_width / 2,
            "y0": self._mmi_length / 2,
            "x1": self._taper_width / 2,
            "y1": self._mmi_length / 2,
            "x2": self._wg_width / 2,
            "y2": self._mmi_length / 2 + self._taper_length,
            "x3": -(self._wg_width / 2),
            "y3": self._mmi_length / 2 + self._taper_length,
            "materialId": SiID,
            "rotate_z": angle,
        }
        lineartrapezoid(cross, "upTaper", uT_attrs)

        uw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                self._mmi_length / 2
                + self._taper_length * 3 / 2
                + self._xy[1],
            ),
        )
        uW_attrs = {
            "x": uw_point[0],
            "x_span": self._wg_width,
            "y": uw_point[1],
            "y_span": self._taper_length,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(cross, "upWg", uW_attrs)

        dT_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": -self._taper_width / 2,
            "y0": -self._mmi_length / 2,
            "x1": self._taper_width / 2,
            "y1": -self._mmi_length / 2,
            "x2": self._wg_width / 2,
            "y2": -(self._mmi_length / 2 + self._taper_length),
            "x3": -(self._wg_width / 2),
            "y3": -(self._mmi_length / 2 + self._taper_length),
            "materialId": SiID,
            "rotate_z": angle,
        }
        lineartrapezoid(cross, "downTaper", dT_attrs)

        uw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                -(self._mmi_length / 2 + self._taper_length * 3 / 2)
                + self._xy[1],
            ),
        )
        dW_attrs = {
            "x": uw_point[0],
            "x_span": self._wg_width,
            "y": uw_point[1],
            "y_span": self._taper_length,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(cross, "downWg", dW_attrs)

        cross.save()
