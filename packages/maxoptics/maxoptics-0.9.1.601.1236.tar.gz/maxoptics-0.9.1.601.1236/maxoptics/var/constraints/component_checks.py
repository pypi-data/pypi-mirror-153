from maxoptics.macros import (
    XYZ_3D,
    X_Normal,
    Y_Normal,
    Z_Normal,
    Point,
    X_Linear,
    Y_Linear,
    Z_Linear,
)


def get_monitor_type(x, y, z):
    _1_0_rep = tuple(1 if _ != 0 else 0 for _ in [x, y, z])

    return {
        (1, 1, 1): XYZ_3D,
        (1, 1, 0): Z_Normal,
        (1, 0, 1): Y_Normal,
        (0, 1, 1): X_Normal,
        (1, 0, 0): X_Linear,
        (0, 1, 0): Y_Linear,
        (0, 0, 1): Z_Linear,
        (0, 0, 0): Point,
    }[_1_0_rep]
