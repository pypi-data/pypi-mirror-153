import numpy as np

from maxoptics.core.plot.GeoBase import _Polygon, _2DPoint

acc = 400
sin = np.sin
cos = np.cos
pi = np.pi


class PolygonLike(_Polygon):
    def __new__(cls, *args):
        instance = super().__new__(cls)
        instance.__init__(*args)
        return instance.to_Polygon()

    @property
    def points(self):
        return []

    def to_Polygon(self):
        return _Polygon(*self.points)


class ComponentLike(PolygonLike):
    def __init__(self, _) -> None:
        """x, y, w, h, theta"""
        # Basic
        self.x = _.get("x")
        self.y = _.get("y")
        self.theta = _.get("rotate_z")

        def _get(k):
            return _.get(k, silent=True)

        # For Rectangle, BezierCurve
        self.w = _get("x_span") or _get("w")
        self.h = _get("y_span")

        # For Triangle, LinearTrapezoid, BezierCurve
        self.x0 = _get("x0")
        self.y0 = _get("y0")
        self.x1 = _get("x1")
        self.y1 = _get("y1")
        self.x2 = _get("x2")
        self.y2 = _get("y2")
        self.x3 = _get("x3")
        self.y3 = _get("y3")

        # For Circle, Sector
        self.r = _get("r") or _get("radius")

        # For Ring, ArcWaveguide
        self.angle = _get("angle")
        self.rin = _get("inner_radius") or _get("innerRadius")
        self.rout = _get("outer_radius") or _get("outerRadius")

        # For Ellipse
        self.xr = _get("xRadius")
        self.yr = _get("yRadius")

        # For CustomPolygon
        self.sides = _get("sides")
        self.size = _get("size")

        # For GdsPolygon
        self._points = _get("points")

    def _shifts(self):
        raise NotImplementedError()

    @property
    def points(self):
        center = np.array([self.x, self.y])
        theta = self.theta / 180 * pi
        rotate = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        )
        deltas = np.dot(self._shifts(), rotate)

        points = [_2DPoint(center + delta) for delta in deltas]
        return points


class Rectangle(ComponentLike):
    def _shifts(self):

        w = self.w
        h = self.h
        return np.array(
            [
                [w / 2, h / 2],
                [-w / 2, h / 2],
                [-w / 2, -h / 2],
                [w / 2, -h / 2],
            ]
        )


class Triangle(ComponentLike):
    def _shifts(self):
        return np.array(
            [[self.x0, self.y0], [self.x1, self.y1], [self.x2, self.y2]]
        )


class Circle(ComponentLike):
    def _shifts(self):
        r = self.r
        return np.multiply(
            [r, r],
            np.array(
                [
                    [cos(_ * pi), sin(_ * pi)]
                    for _ in [2 * i / acc for i in range(acc)]
                ]
            ),
        )


class Ring(ComponentLike):
    def _shifts(self):
        rout = self.rout
        rin = self.rin
        diff = np.multiply(
            [rout, rout],
            list(
                map(
                    lambda _: [cos(_ * pi), sin(_ * pi)],
                    [2 * i / acc for i in range(acc + 1)],
                )
            ),
        )
        hole = np.multiply(
            [rin, rin],
            list(
                map(
                    lambda _: [cos(_ * pi), sin(_ * pi)],
                    [-2 * i / acc for i in range(acc + 1)],
                )
            ),
        )
        return np.vstack((diff, hole))


class Sector(ComponentLike):
    def _shifts(self):
        temp = list(
            map(
                lambda _: [cos(_ * pi), sin(_ * pi)],
                [
                    (2 * i / acc) * (self.angle / 360)
                    for i in range(acc, -1, -1)
                ],
            )
        )
        temp.insert(0, [0, 0])
        temp.append([0, 0])
        radius = self.r
        diff = np.multiply([radius, -radius], temp)
        return diff


class LinearTrapezoid(ComponentLike):
    def _shifts(self):
        diff = np.array(
            [
                [self.x0, self.y0],
                [self.x1, self.y1],
                [self.x2, self.y2],
                [self.x3, self.y3],
            ]
        )
        return diff


class ArcWaveguide(ComponentLike):
    def _shifts(self):
        temp_out = list(
            map(
                lambda _: [
                    cos(_ * pi) * self.rout,
                    sin(_ * pi) * (-self.rout),
                ],
                [
                    (2 * i / acc) * (self.angle / 360)
                    for i in range(acc, -1, -1)
                ],
            )
        )
        temp_in = list(
            map(
                lambda _: [cos(_ * pi) * self.rin, sin(_ * pi) * (-self.rin)],
                [(2 * i / acc) * (self.angle / 360) for i in range(acc + 1)],
            )
        )
        temp_out.extend(temp_in)
        temp_out.append(temp_out[0])
        diff = np.array(temp_out)
        return diff


class BezierCurve(ComponentLike):
    def _shifts(self):
        w = self.w
        fourpoints = np.array(
            [
                [self.x0, self.y0],
                [self.x1, self.y1],
                [self.x2, self.y2],
                [self.x3, self.y3],
            ]
        )

        def bezier_points():
            def bezier_ratios(acc):
                for i in range(acc + 1):
                    a = i / acc
                    yield [
                        [
                            (1 - a) ** 3,
                            3 * a * ((1 - a) ** 2),
                            3 * (1 - a) * (a ** 2),
                            a ** 3,
                        ],
                        [
                            -3 * (1 - a) ** 2,
                            3 * ((1 - a) ** 2 - 2 * a * (1 - a)),
                            3 * (2 * a * (1 - a) - a ** 2),
                            3 * a ** 2,
                        ],
                    ]

            for ratio in bezier_ratios(acc):
                yield [
                    np.dot(ratio[0], fourpoints),
                    np.dot(ratio[1], fourpoints),
                ]

        diff = [[], []]
        for p in bezier_points():
            try:
                delta = p[1]
                p = p[0]
                normal_vector = np.c_[delta[1], -delta[0]] / (
                    (delta ** 2).sum() ** (1 / 2)
                )
                diff[0].append((p + normal_vector * w / 2)[0])
                diff[1].append((p - normal_vector * w / 2)[0])
            except StopIteration:
                break
        diff[1].reverse()
        diff = diff[0] + diff[1]
        return np.array(diff)


SCurve = BezierCurve


class Ellipse(ComponentLike):
    def _shifts(self):
        diff = np.multiply(
            [self.xr, self.yr],
            list(
                map(
                    lambda _: [cos(_ * pi), sin(_ * pi)],
                    [2 * i / acc for i in range(acc)],
                )
            ),
        )
        return diff


class CustomPolygon(ComponentLike):
    def _shifts(self):
        sides = self.sides
        size = self.size

        if sides < 3:
            sides = 3
        basepoint = [size, 0]
        pointset = []
        for i in range(0, sides + 2):
            if i > sides:
                pointset.append(basepoint)
            else:
                pointset.append(
                    [
                        size * cos(i * 2 * pi / sides),
                        size * sin(i * 2 * pi / sides),
                    ]
                )
        return pointset


class GdsPolygon(ComponentLike):
    def _shifts(self):
        return self._points


def compromised_transform(_) -> ComponentLike:
    """This method will be expired in the future, because all `Project Component` object will become instance of static
    derived class instead of runtime class.

    Args:
        _ (ProjectComponent): Only Polygon object are supported. It will raise KeyError if other input is given.

    Returns:
        _Polygon: A class with contain-point checking and self-draw method.

    """
    cls = {
        "Rectangle": Rectangle,
        "Triangle": Triangle,
        "Circle": Circle,
        "Ring": Ring,
        "Sector": Sector,
        "LinearTrapezoid": LinearTrapezoid,
        "ArcWaveguide": ArcWaveguide,
        "BezierCurve": BezierCurve,
        "Ellipse": Ellipse,
        "CustomPolygon": CustomPolygon,
        "GdsPolygon": GdsPolygon,
    }
    return cls[_.type.name](_)
