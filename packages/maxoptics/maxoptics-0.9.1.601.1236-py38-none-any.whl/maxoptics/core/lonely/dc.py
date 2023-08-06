from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import rotate_point, rectangle, beziercurve
from maxoptics.var.project import MosProject
from maxoptics.sdk import MaxOptics
from maxoptics import MosLibrary


class DC(Device):
    def __init__(
        self,
        xy=(0, 0),
        gap=0.1,
        coupler_length=2,
        wg_width=0.4,
        total_length=10,
        total_width=8,
    ) -> None:
        super().__init__(xy)
        self._coupler_length = coupler_length
        self._gap = gap
        self._wg_width = wg_width
        self._total_length = total_length
        self._total_width = total_width

    def build(self, dc: MosProject, material, angle=0):
        SiID = material
        in_length = 3
        bc_length = self._total_length - in_length

        ugw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                self._gap / 2 + self._wg_width / 2 + self._xy[1],
            ),
        )
        ugw_attrs = {
            "x": ugw_point[0],
            "y": ugw_point[1],
            "x_span": self._coupler_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(dc, "upGapWg", ugw_attrs)

        ugw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                self._xy[1] - (self._gap / 2 + self._wg_width / 2),
            ),
        )
        dgw_attrs = {
            "x": ugw_point[0],
            "y": ugw_point[1],
            "x_span": self._coupler_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(dc, "downGapWg", dgw_attrs)

        ulbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": -(bc_length + self._coupler_length / 2),
            "y0": self._total_width / 2,
            "x1": -(bc_length + self._coupler_length / 2) + 2.5,
            "y1": self._total_width / 2,
            "x2": -(bc_length + self._coupler_length / 2) + 2.5,
            "y2": self._gap / 2 + self._wg_width / 2,
            "x3": -(self._coupler_length / 2),
            "y3": self._gap / 2 + self._wg_width / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(dc, "upLeftBc", ulbc_attrs)

        dlbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": -(bc_length + self._coupler_length / 2),
            "y0": -self._total_width / 2,
            "x1": -(bc_length + self._coupler_length / 2) + 2.5,
            "y1": -self._total_width / 2,
            "x2": -(bc_length + self._coupler_length / 2) + 2.5,
            "y2": -(self._gap / 2 + self._wg_width / 2),
            "x3": -(self._coupler_length / 2),
            "y3": -(self._gap / 2 + self._wg_width / 2),
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(dc, "downLeftBc", dlbc_attrs)

        ilw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                -(self._coupler_length / 2 + bc_length + 1.5) + self._xy[0],
                self._total_width / 2 + self._xy[1],
            ),
        )
        ilw_attrs = {
            "x": ilw_point[0],
            "y": ilw_point[1],
            "x_span": in_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(dc, "inLeftWg", ilw_attrs)

        olw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                -(self._coupler_length / 2 + bc_length + 1.5) + self._xy[0],
                -self._total_width / 2 + self._xy[1],
            ),
        )
        olw_attrs = {
            "x": olw_point[0],
            "y": olw_point[1],
            "x_span": in_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(dc, "outLeftWg", olw_attrs)

        urbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": (bc_length + self._coupler_length / 2),
            "y0": self._total_width / 2,
            "x1": (bc_length + self._coupler_length / 2) - 2.5,
            "y1": self._total_width / 2,
            "x2": (bc_length + self._coupler_length / 2) - 2.5,
            "y2": self._gap / 2 + self._wg_width / 2,
            "x3": (self._coupler_length / 2),
            "y3": self._gap / 2 + self._wg_width / 2,
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(dc, "upRightBc", urbc_attrs)

        drbc_attrs = {
            "x": self._xy[0],
            "y": self._xy[1],
            "z_span": self._height,
            "w": self._wg_width,
            "x0": (bc_length + self._coupler_length / 2),
            "y0": -self._total_width / 2,
            "x1": (bc_length + self._coupler_length / 2) - 2.5,
            "y1": -self._total_width / 2,
            "x2": (bc_length + self._coupler_length / 2) - 2.5,
            "y2": -(self._gap / 2 + self._wg_width / 2),
            "x3": (self._coupler_length / 2),
            "y3": -(self._gap / 2 + self._wg_width / 2),
            "materialId": SiID,
            "rotate_z": angle,
        }
        beziercurve(dc, "downRightBc", drbc_attrs)

        irw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                (self._coupler_length / 2 + bc_length + 1.5) + self._xy[0],
                self._total_width / 2 + self._xy[1],
            ),
        )
        irw_attrs = {
            "x": irw_point[0],
            "y": irw_point[1],
            "x_span": in_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(dc, "inRightWg", irw_attrs)

        orw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                (self._coupler_length / 2 + bc_length + 1.5) + self._xy[0],
                -self._total_width / 2 + self._xy[1],
            ),
        )
        oRw_attrs = {
            "x": orw_point[0],
            "y": orw_point[1],
            "x_span": in_length,
            "y_span": self._wg_width,
            "z_span": self._height,
            "materialId": SiID,
            "rotate_z": angle,
        }
        rectangle(dc, "intLeftWgDown", oRw_attrs)
        dc.save()

