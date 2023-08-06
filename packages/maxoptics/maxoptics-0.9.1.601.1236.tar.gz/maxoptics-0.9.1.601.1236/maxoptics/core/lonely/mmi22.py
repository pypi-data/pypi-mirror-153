from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import (
    lineartrapezoid,
    rotate_point,
    rectangle,
)
from maxoptics.var.project import MosProject


class MMI4Port(Device):
    def __init__(
        self,
        xy=(0, 0),
        wg_width=0.5,
        taper_width=0.8,
        mmi_width=3.6,
        taper_length=2,
        mmi_length=8.5,
        gap=1,
    ) -> None:
        super().__init__(xy)
        self._wg_width = wg_width
        self._taper_width = taper_width
        self._mmi_width = mmi_width
        self._taper_length = taper_length
        self._mmi_length = mmi_length
        self._gap = gap

    def build(self, mmi: MosProject, material, angle=0):
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
        mmiWg = mmi.add("Rectangle", "mmiWg")
        mmiWg.update(mmiwg_attrs)

        ult_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": -(self._mmi_length / 2),
            "y0": self._gap / 2 + self._taper_width / 2,
            "x1": -(self._mmi_length / 2),
            "y1": self._gap / 2 - self._taper_width / 2,
            "x2": -(self._mmi_length / 2) - self._taper_length,
            "y2": self._gap / 2 - self._wg_width / 2,
            "x3": -(self._mmi_length / 2) - self._taper_length,
            "y3": self._gap / 2 + self._wg_width / 2,
            "rotate_z": angle,
            "materialId": SiID,
        }
        lineartrapezoid(mmi, "upLeftTaper", ult_attrs)

        dlt_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "x0": -(self._mmi_length / 2),
            "y0": -(self._gap / 2 + self._taper_width / 2),
            "x1": -(self._mmi_length / 2),
            "y1": -(self._gap / 2 - self._taper_width / 2),
            "x2": -(self._mmi_length / 2) - self._taper_length,
            "y2": -(self._gap / 2 - self._wg_width / 2),
            "x3": -(self._mmi_length / 2) - self._taper_length,
            "y3": -(self._gap / 2 + self._wg_width / 2),
            "materialId": SiID,
            "rotate_z": angle,
        }
        lineartrapezoid(mmi, "downLeftTaper", dlt_attrs)

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
        lineartrapezoid(mmi, "upRightTaper", urt_attrs)

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
        lineartrapezoid(mmi, "downRightTaper", drt_attrs)

        ulw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                -(self._mmi_length / 2) - self._taper_length - 1 + self._xy[0],
                self._gap / 2 + self._xy[1],
            ),
        )
        ulw_attrs = {
            "x_span": 2,
            "x": ulw_point[0],
            "y_span": self._wg_width,
            "y": ulw_point[1],
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mmi, "upLeftwg", ulw_attrs)

        dlw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                -(self._mmi_length / 2) - self._taper_length - 1 + self._xy[0],
                -(self._gap / 2) + self._xy[1],
            ),
        )
        dlw_attrs = {
            "x_span": 2,
            "x": dlw_point[0],
            "y_span": self._wg_width,
            "y": dlw_point[1],
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mmi, "downLeftwg", dlw_attrs)

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
            "y_span": self._wg_width,
            "y": urw_point[1],
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mmi, "upRightwg", urw_attrs)

        drw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                (self._mmi_length / 2) + self._taper_length + 1 + self._xy[0],
                -(self._gap / 2) + self._xy[1],
            ),
        )
        drw_attrs = {
            "x_span": 2,
            "x": drw_point[0],
            "y_span": self._wg_width,
            "y": drw_point[1],
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mmi, "downRightwg", drw_attrs)
        mmi.save()
