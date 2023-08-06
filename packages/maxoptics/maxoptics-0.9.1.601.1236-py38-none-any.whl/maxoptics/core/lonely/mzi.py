from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.mmi12 import MMI3Port as MMI
from maxoptics.core.lonely.sdkbuild import rectangle, beziercurve
from maxoptics.core.lonely.sdkbuild import rotate_point
from maxoptics.var.project import MosProject
from maxoptics.sdk import MaxOptics


class MZI(Device):
    def __init__(
        self,
        xy=(0, 0),
        wg_width=0.5,
        taper_width=0.8,
        taper_length=2,
        gap=1,
        mmi_width=2.2,
        mmi_length=4.4,
        delta_l=0.5,
    ) -> None:
        super().__init__(xy)
        self._wg_width = wg_width
        self._taper_width = taper_width
        self._taper_length = taper_length
        self._gap = gap
        self._mmi_width = mmi_width
        self._mmi_length = mmi_length
        self._delta_l = delta_l

    def build(self, mzi: MosProject, material, angle=0):
        SiID = material

        uw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                self._xy[1] + 4 + self._gap / 2,
            ),
        )
        uw_attrs = {
            "x": uw_point[0],
            "y": uw_point[1],
            "x_span": 4,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mzi, "upWg", uw_attrs)

        dw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                self._xy[1] - (4 + self._delta_l + self._gap / 2),
            ),
        )
        dw_attrs = {
            "x": dw_point[0],
            "y": dw_point[1],
            "x_span": 4,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(mzi, "downWg", dw_attrs)

        urbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": 5,
            "y0": self._gap / 2,
            "x1": 2,
            "y1": self._gap / 2,
            "x2": 5,
            "y2": 4 + self._gap / 2,
            "x3": 2,
            "y3": 4 + self._gap / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(mzi, "upRightBc", urbc_attrs)

        ulbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": -5,
            "y0": self._gap / 2,
            "x1": -2,
            "y1": self._gap / 2,
            "x2": -5,
            "y2": 4 + self._gap / 2,
            "x3": -2,
            "y3": 4 + self._gap / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(mzi, "upLeftBc", ulbc_attrs)

        mmileft_center = rotate_point(
            angle,
            [
                self._xy[0],
                self._xy[1],
                self._xy[0] - (7 + self._taper_length + self._mmi_length / 2),
                self._xy[1],
            ],
        )
        mmi_left = MMI(
            xy=mmileft_center,
            wg_width=self._wg_width,
            taper_width=self._taper_width,
            taper_length=self._taper_length,
            gap=self._gap,
            mmi_width=self._mmi_width,
            mmi_length=self._mmi_length,
        )
        mmi_left.build(mzi, SiID, angle)

        mmiright_center = rotate_point(
            angle,
            [
                self._xy[0],
                self._xy[1],
                self._xy[0] + 7 + self._taper_length + self._mmi_length / 2,
                self._xy[1],
            ],
        )
        mmi_right = MMI(
            xy=mmiright_center,
            wg_width=self._wg_width,
            taper_width=self._taper_width,
            taper_length=self._taper_length,
            gap=self._gap,
            mmi_width=self._mmi_width,
            mmi_length=self._mmi_length,
        )
        mmi_right.build(mzi, SiID, angle + 180, name="L")

        drbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": 5,
            "y0": -(self._gap / 2),
            "x1": 2,
            "y1": -(self._gap / 2),
            "x2": 5,
            "y2": -(4 + self._gap / 2 + self._delta_l),
            "x3": 2,
            "y3": -(4 + self._gap / 2 + self._delta_l),
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(mzi, "downRightBc", drbc_attrs)

        dlbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": -(5),
            "y0": -(self._gap / 2),
            "x1": -(2),
            "y1": -(self._gap / 2),
            "x2": -(5),
            "y2": -(4 + self._gap / 2 + self._delta_l),
            "x3": -(2),
            "y3": -(4 + self._gap / 2 + self._delta_l),
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(mzi, "downLeftBc", dlbc_attrs)

        mzi.save()


if __name__ == "__main__":
    client = MaxOptics()
    project = client.create_project_as("MZI.passive")
    SiID = client.public_materials["Si (Silicon) - Palik"]["id"]

    mzi = MZI()
    mzi.build(project, SiID)
    mzi.visuilize(project, xysize=(20, 20))
