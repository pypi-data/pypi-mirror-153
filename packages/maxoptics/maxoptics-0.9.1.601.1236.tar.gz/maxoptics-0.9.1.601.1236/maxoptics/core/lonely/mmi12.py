from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import (
    rectangle,
    lineartrapezoid,
    rotate_point,
)
from maxoptics.var.project import MosProject


class MMI3Port(Device):
    def __init__(
        self,
        xy=(0, 0),
        wg_width=0.5,
        taper_width=0.8,
        taper_length=2,
        gap=1,
        mmi_width=2.2,
        mmi_length=4.4,
    ) -> None:
        super().__init__(xy)
        self._wg_width = wg_width
        self._taper_width = taper_width
        self._taper_length = taper_length
        self._gap = gap
        self._mmi_width = mmi_width
        self._mmi_length = mmi_length

    def build(self, mmi: MosProject, material, angle=0, name=""):
        SiID = material

        mmiwg_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "x_span": self._mmi_length,
            "y_span": self._mmi_width,
            "z_span": self._height,
            "rotate_z": angle,
            "materialId": SiID,
        }
        rectangle(mmi, "mmiWg" + name, mmiwg_attrs)

        lt_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": -(self._mmi_length / 2),
            "y0": self._taper_width / 2,
            "x1": -(self._mmi_length / 2),
            "y1": -self._taper_width / 2,
            "x2": -(self._mmi_length / 2) - self._taper_length,
            "y2": -self._wg_width / 2,
            "x3": -(self._mmi_length / 2) - self._taper_length,
            "y3": self._wg_width / 2,
            "rotate_z": angle,
            "materialId": SiID,
        }
        lineartrapezoid(mmi, "leftTaper" + name, lt_attrs)

        lw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                -(self._mmi_length / 2) - self._taper_length - 1 + self._xy[0],
                self._xy[1],
            ),
        )
        lw_attrs = {
            "x": lw_point[0],
            "y": lw_point[1],
            "x_span": 2,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mmi, "leftWg" + name, lw_attrs)

        urt_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": self._mmi_length / 2,
            "y0": self._gap / 2 + self._taper_width / 2,
            "x1": self._mmi_length / 2,
            "y1": self._gap / 2 - self._taper_width / 2,
            "x2": self._mmi_length / 2 + self._taper_length,
            "y2": self._gap / 2 - self._wg_width / 2,
            "x3": self._mmi_length / 2 + self._taper_length,
            "y3": self._gap / 2 + self._wg_width / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        lineartrapezoid(mmi, "upRightTaper" + name, urt_attrs)

        drt_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": self._mmi_length / 2,
            "y0": -(self._gap / 2 + self._taper_width / 2),
            "x1": self._mmi_length / 2,
            "y1": -(self._gap / 2 - self._taper_width / 2),
            "x2": self._mmi_length / 2 + self._taper_length,
            "y2": -(self._gap / 2 - self._wg_width / 2),
            "x3": self._mmi_length / 2 + self._taper_length,
            "y3": -(self._gap / 2 + self._wg_width / 2),
            "materialId": SiID,
            "rotate_z": angle,
        }
        lineartrapezoid(mmi, "downRightTaper" + name, drt_attrs)

        urw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._mmi_length / 2 + self._taper_length + 1 + self._xy[0],
                self._gap / 2 + self._xy[1],
            ),
        )
        urw_attrs = {
            "x_span": 2,
            "x": urw_point[0],
            "y": urw_point[1],
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mmi, "upRightWg" + name, urw_attrs)

        drw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._mmi_length / 2 + self._taper_length + 1 + self._xy[0],
                -(self._gap / 2) + self._xy[1],
            ),
        )
        drw_attrs = {
            "x_span": 2,
            "x": drw_point[0],
            "y": drw_point[1],
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mmi, "downRightWg" + name, drw_attrs)
        mmi.save()
