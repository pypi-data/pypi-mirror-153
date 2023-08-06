from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.mmi12 import MMI3Port as MMI
from maxoptics.core.lonely.sdkbuild import beziercurve
from maxoptics.var.project import MosProject


class Spliter(Device):
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

    def build(self, spliter: MosProject, material, angle=0):
        SiID = material

        mmi = MMI(
            xy=(self._xy[0], self._xy[1]),
            wg_width=self._wg_width,
            taper_width=self._taper_width,
            taper_length=self._taper_length,
            gap=self._gap,
            mmi_width=self._mmi_width,
            mmi_length=self._mmi_length,
        )
        mmi.build(spliter, SiID, angle)

        ulbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": self._mmi_length / 2 + self._taper_length + 2,
            "y0": self._gap / 2,
            "x1": self._mmi_length / 2 + self._taper_length + 5,
            "y1": self._gap / 2,
            "x2": self._mmi_length / 2 + self._taper_length + 2,
            "y2": 4 + self._gap / 2,
            "x3": self._mmi_length / 2 + self._taper_length + 5,
            "y3": 4 + self._gap / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(spliter, "upBc", ulbc_attrs)

        dlbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": self._mmi_length / 2 + self._taper_length + 2,
            "y0": -(self._gap / 2),
            "x1": self._mmi_length / 2 + self._taper_length + 5,
            "y1": -(self._gap / 2),
            "x2": self._mmi_length / 2 + self._taper_length + 2,
            "y2": -(4 + self._gap / 2),
            "x3": self._mmi_length / 2 + self._taper_length + 5,
            "y3": -(4 + self._gap / 2),
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(spliter, "downBc", dlbc_attrs)

        spliter.save()
