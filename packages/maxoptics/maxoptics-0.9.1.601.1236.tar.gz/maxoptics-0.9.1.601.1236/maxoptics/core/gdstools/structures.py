from .GdsTypes import Cube3D


def ex(v):
    return round(v * 1000) / 1000


def attrValue(obj, str_atti):
    arr = str_atti.split(".")
    for i in range(0, len(arr)):
        obj = getattr(obj, arr[i])
    return obj


class Structure:
    @classmethod
    def addToProject(self, index, polygon, material, layer, project) -> object:
        """
        将多边形加入project
        """
        self.index = index
        self.project = project
        self.material = material
        self.polygon = polygon
        self.layer = layer
        return self.__polygonToProject()

    @classmethod
    def __polygonToProject(self) -> object:
        obj_name = "PointsPolygon" if self.layer is None else "GdsPolygon"
        obj = self.project.add("GdsPolygon")
        obj.name = "%s%d" % (obj_name, self.index)
        # obj["spatial"] = {
        #     "rotateX": 0,
        #     "rotateY": 0,
        #     "rotateZ": 0,
        #     "x": 0,
        #     "y": 0,
        #     "z": 0,
        # }

        if self.material is not None:
            obj["materialId"] = self.material.iloc[0].at["id"]

        obj["points"] = self.__polygonToPoints()
        if self.layer is not None:
            obj["z"] = self.layer["z"] + self.layer["h"] / 2
            obj["h"] = self.layer["h"]
            obj["z_min"] = self.layer["zmin"]
            obj["z_max"] = self.layer["zmax"]
            obj["z_span"] = self.layer["h"]
        else:
            obj["z"] = 0
            obj["h"] = 1
            obj["z_min"] = -0.5
            obj["z_max"] = 0.5
            obj["z_span"] = 1
        obj["rotate_z"] = 0
        return obj

    @classmethod
    def __polygonToPoints(self):
        """
        点列表进入 meshgen : 顺时针识别为空心洞, 逆时针识别为实心图;
        """
        points = []
        for p in self.polygon:
            points.append([p[0], p[1]])
        if not self.__isAntiClockWise(points):
            points.reverse()
        return points

    @classmethod
    def __isAntiClockWise(self, points):
        """
        利用格林公式: 求出每个向量的曲线积分，计算出代数和，如果为正值，即为逆时针。
        """
        sum = 0
        last = len(points)
        for i in range(0, last):
            p1 = points[i]
            p2 = points[0 if (i >= (last - 1)) else (i + 1)]
            sum += -0.5 * (p2[0] - p1[0]) * (p2[1] + p1[1])
        return sum > 0

    @classmethod
    def __polygonToRectangle(self) -> object:
        """
        多边形转长方形
        """
        v = Cube3D(self.polygon, self.layer)
        obj = self.project.add("Rectangle")
        obj.name = "Rectangle%d" % (self.index)
        obj["spatial"] = {
            "rotateX": 0,
            "rotateY": 0,
            "rotateZ": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }

        # 定义赋值的key组. [dst name, src name]
        attrs = [
            ["x", "position.x"],
            ["x_min", "range.x.min"],
            ["x_max", "range.x.max"],
            ["x_span", "size.x"],
            ["y", "position.y"],
            ["y_min", "range.y.min"],
            ["y_max", "range.y.max"],
            ["y_span", "size.y"],
            ["z", "position.z"],
            ["z_min", "range.z.min"],
            ["z_max", "range.z.max"],
            ["z_span", "size.z"],
        ]

        for item in attrs:
            key = item[0]
            value = ex(attrValue(v, item[1]))
            obj[key] = value
        obj["rotate_z"] = 0

        obj["materialId"] = self.material.iloc[0].at["id"]

        return obj
