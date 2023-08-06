"""General Solver (bad accuracy)"""
from abc import ABCMeta, abstractmethod
from functools import partial
from typing import List, Iterable, Callable

import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path


class _2DPoint:
    def __init__(self, coordinate) -> None:
        self.coordinate = np.array(coordinate, dtype=np.float64)

    def __sub__(self, other):
        return Segment(self, other)

    def __add__(self, other):
        return _Polygon(self, other)

    def __iter__(self):
        return iter(self.coordinate)

    def __str__(self):
        return "_2DPoint: {}".format(self.coordinate)


class _Polygon:
    def __init__(self, *points) -> None:
        self.points: List[_2DPoint] = list(points)

    def __add__(self, point: _2DPoint):
        return _Polygon(*self.points, point)

    def __plot__(self, facecolor=None):
        path = Path([tuple(_) for _ in self.points])
        patch = patches.PathPatch(path, facecolor=facecolor, lw=0)
        return patch

    def __contains__(self, m: Iterable):
        """Ray method

        Args:
            m (_2DPoint): Point

        Returns:
            bool: in or not in.
        """
        if any([seg.through(m) for seg in self.segments]):
            return True

        # Horizontal line
        ray = Line(m, 0)

        def _only_accept_positive(self, line_like: LineLike):
            center = line_like.center
            return self.point[0] < center[0]

        ray.checker = _only_accept_positive
        cross = len(set([result for seg in self.segments if (result := ray & seg)]))
        return cross % 2 == 1

    @property
    def segments(self):
        return [
            sp - ep
            for i in range(len(self.points))
            if (sp := self.points[i - 1]) and (ep := self.points[i])
        ]


class LineLike(metaclass=ABCMeta):
    @property
    @abstractmethod
    def center(self):
        return []

    @property
    @abstractmethod
    def A(self):
        return []

    def __and__(self, other):
        conditions = [(self.condition, other), (other.condition, self)]
        for condition, args in conditions:
            if not condition(args):
                return ()
        A = np.vstack((self.A, other.A))
        b = np.array([np.dot(self.center, self.A), np.dot(other.center, other.A)])
        try:
            result = np.dot(np.linalg.inv(A), b)
        except np.linalg.LinAlgError:
            # Singular matrix
            return ()

        return tuple(result)

    @property
    def condition(self) -> Callable:
        return partial(self.checker, self)


class Segment(LineLike):
    def __init__(self, start_point: _2DPoint, end_point: _2DPoint) -> None:
        self.start_point = start_point
        self.end_point = end_point

        def checker(self, line_like: LineLike):
            A = line_like.A
            x1 = list(self.start_point)
            x2 = list(self.end_point)
            b = np.dot(A, line_like.center)
            return (np.dot(A, x1) - b) * (np.dot(A, x2) - b) <= 0

        self.checker = checker

    @property
    def center(self):
        return (self.start_point.coordinate + self.end_point.coordinate) / 2

    @property
    def A(self):
        _seg = self.end_point.coordinate - self.start_point.coordinate
        theta = np.arctan2(_seg[1], _seg[0])
        return np.array([np.sin(theta), -np.cos(theta)])

    def through(self, _: tuple):
        return abs(np.dot(self.A, self.center) - np.dot(self.A, _)) < 1e-12


class Line(LineLike):
    def __init__(self, point, angle_info) -> None:
        self.point = np.array(list(point))
        if isinstance(angle_info, Iterable):
            self.angle_info = np.array(angle_info).astype(np.float64)
        else:
            self.angle_info = np.array([np.sin(angle_info), -np.cos(angle_info)]).astype(
                np.float64
            )

        def checker(self, line_like):
            return True

        self.checker = checker

    @property
    def center(self):
        return self.point

    @property
    def A(self):
        return self.angle_info
