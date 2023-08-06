from maxoptics.core.lonely.device import Device
from maxoptics.core.lonely.sdkbuild import rotate_point
from maxoptics.var.project import MosProject


class RingResonators(Device):
    def __init__(
        self, xy=(0, 0), wg_width=0.4, r=2.9, length=2, gap=0.1
    ) -> None:
        super().__init__(xy)
        self.wgWidth = wg_width
        self.r = r
        self.length = length
        self.gap = gap

    def build(self, R: MosProject, material, angle=0):
        lc_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                -(self.length / 2) + self._xy[0],
                self._xy[1],
            ),
        )
        SiID = material
        leftCircle = R.add("ArcWaveguide", "leftCircle")
        leftCircle["x"] = lc_point[0]
        leftCircle["y"] = lc_point[1]
        leftCircle["z_span"] = self._height
        leftCircle["innerRadius"] = self.r
        leftCircle["outerRadius"] = self.r + self.wgWidth
        leftCircle["angle"] = 180
        leftCircle["rotate_z"] = 90 + angle
        leftCircle["materialId"] = SiID
        leftCircle["meshOrder"] = 2

        rc_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self.length / 2 + self._xy[0],
                self._xy[1],
            ),
        )
        rightCircle = R.add("ArcWaveguide", "rightCircle")
        rightCircle["x"] = rc_point[0]
        rightCircle["y"] = rc_point[1]
        rightCircle["z_span"] = self._height
        rightCircle["innerRadius"] = self.r
        rightCircle["outerRadius"] = self.r + self.wgWidth
        rightCircle["angle"] = 180
        rightCircle["rotate_z"] = 270 + angle
        rightCircle["materialId"] = SiID
        rightCircle["meshOrder"] = 2

        uc_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                self.r + self.wgWidth / 2 + self._xy[1],
            ),
        )
        upRect = R.add("Rectangle", "upRect")
        upRect["x"] = uc_point[0]
        upRect["x_span"] = self.length
        upRect["y"] = uc_point[1]
        upRect["y_span"] = self.wgWidth
        upRect["z_span"] = self._height
        upRect["materialId"] = SiID
        upRect["rotate_z"] = angle

        dc_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                -(self.r + self.wgWidth / 2) + self._xy[1],
            ),
        )
        downRect = R.add("Rectangle", "downRect")
        downRect["x"] = dc_point[0]
        downRect["x_span"] = self.length
        downRect["y"] = dc_point[1]
        downRect["y_span"] = self.wgWidth
        downRect["z_span"] = self._height
        downRect["materialId"] = SiID
        downRect["rotate_z"] = angle

        iw_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                self.r
                + self.wgWidth
                + self.gap
                + self.wgWidth / 2
                + self._xy[1],
            ),
        )
        inWg = R.add("Rectangle", "inWg")
        inWg["x"] = iw_point[0]
        inWg["x_span"] = 12 + self.length
        inWg["y"] = iw_point[1]
        inWg["y_span"] = self.wgWidth
        inWg["z_span"] = self._height
        inWg["materialId"] = SiID
        inWg["rotate_z"] = angle

        ow_point = rotate_point(
            angle,
            (
                self._xy[0],
                self._xy[1],
                self._xy[0],
                -(self.r + self.wgWidth + self.gap + self.wgWidth / 2)
                + self._xy[1],
            ),
        )
        outWg = R.add("Rectangle", " outWg")
        outWg["x"] = ow_point[0]
        outWg["x_span"] = 12 + self.length
        outWg["y"] = ow_point[1]
        outWg["y_span"] = self.wgWidth
        outWg["z_span"] = self._height
        outWg["materialId"] = SiID
        outWg["rotate_z"] = angle
        R.save()
