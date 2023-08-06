import math

import numpy as np

from maxoptics.sdk import MaxOptics


def rectangle(project: MaxOptics, name: str, args: dict):
    rectangle = project.add("Rectangle", name)
    put_attrs(rectangle, args)
    return rectangle


def arcwaveguide(project: MaxOptics, name: str, args: dict):
    arcwaveguide = project.add("ArcWaveguide", name)
    put_attrs(arcwaveguide, args)
    return arcwaveguide


def lineartrapezoid(project: MaxOptics, name: str, args: dict):
    lineartrapezoid = project.add("LinearTrapezoid", name)
    put_attrs(lineartrapezoid, args)


def beziercurve(project: MaxOptics, name: str, args: dict):
    beziercurve = project.add("BezierCurve", name)
    put_attrs(beziercurve, args)


def fdtd(project: MaxOptics, args: dict):
    fdtd = project.add("FDTD")
    put_attrs(fdtd, args)


def eme(project: MaxOptics, args: dict):
    eme = project.add("EME")
    put_attrs(eme, args)


def modesource(project: MaxOptics, name: str, args: dict):
    modesource = project.add("ModeSource", name)
    put_attrs(modesource, args)


def powermonitor(project: MaxOptics, name: str, args: dict):
    powermonitor = project.add("PowerMonitor", name)
    put_attrs(powermonitor, args)


def port(project: MaxOptics, name: str, args: dict):
    port = project.add("EmePort", name)
    put_attrs(port, args)


def profilemonitor(project: MaxOptics, name: str, args: dict):
    profilemonitor = project.add("ProfileMonitor", name)
    put_attrs(profilemonitor, args)


def put_attrs(project, args):
    for k, v in args.items():
        if k in project.__dict__["attrs"].__dict__.keys():
            project[k] = v
        else:
            print(f"{k} not in attrs")


def rotate_point(angle, xy: list):
    """
    xy: [x0,y0,x1,y2]
    (x0,y0): center point
    (x1,y1): start point
    """

    d_angle = angle
    xy_angle = np.arctan2(xy[3] - xy[1], xy[2] - xy[0]) * 180 / np.pi
    final_angle = xy_angle - d_angle

    r = math.sqrt((xy[2] - xy[0]) ** 2 + (xy[3] - xy[1]) ** 2)
    x = xy[0] + r * np.cos(final_angle * np.pi / 180)
    y = xy[1] + r * np.sin(final_angle * np.pi / 180)

    return (x, y)
