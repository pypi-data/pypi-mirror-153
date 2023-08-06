class Point3D:
    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
        self.z = p[2] or 0.0


class Range3D:
    def __init__(self, p):
        self.min = p[0]
        self.max = p[1]


class Cube3D:
    def __init__(self, polygon, layer):
        """
        图形初始锚点位于图形视觉中心;
        """
        min_x = min(polygon, key=lambda item: item[0])[0]
        max_x = max(polygon, key=lambda item: item[0])[0]
        min_y = min(polygon, key=lambda item: item[1])[1]
        max_y = max(polygon, key=lambda item: item[1])[1]
        # 调整精度

        self.position = Point3D([0, 0, 0])
        self.position.x = (max_x - min_x) / 2
        self.position.y = (max_y - min_y) / 2
        self.position.z = layer["z"]

        self.size = Point3D([0, 0, 0])
        self.size.x = max_x - min_x
        self.size.y = max_y - min_y
        self.size.z = layer["h"]

        self.range = Point3D([None, None, None])
        self.range.x = Range3D([min_x, max_x])
        self.range.y = Range3D([min_y, max_y])
        self.range.z = Range3D([layer["zmin"], layer["zmax"]])
        return
