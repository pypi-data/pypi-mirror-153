from copy import deepcopy
from functools import partial
from math import inf

import numpy as np
from numpy import pi

from maxoptics.core.base.BaseDataCls import MaterialPart
from maxoptics.var.project import MosProject
from maxoptics.core.plot.GeoBase import Line
from maxoptics.core.plot.PolygonLike import compromised_transform
from maxoptics.sdk import MaxOptics


def __get_nearest_permittivity(table_data, wavelength):
    if "table_head" in table_data:
        table_data.pop("table_head")
    if "anisotropy" in table_data:
        table_data.pop("anisotropy")
    _table = table_data["table_data"]
    result_w, result_p, delta_w = None, None, inf
    for _dict in _table:
        this_wavelen = _dict["wavelength_frequency"]
        this_indexes = [_dict["re"], _dict["im"]]
        this_delta = abs(wavelength - float(this_wavelen))
        if delta_w > this_delta:
            delta_w = this_delta
            result_w = float(this_wavelen)
            result_p = [float(_) for _ in this_indexes]

    if not result_w or not result_p:
        raise ValueError("Material permittivity data can not be empty!")

    return result_w, result_p


def __get_material_permittivity(client: MaxOptics, material_id, wavelength):
    materials = client.user_materials.all() + client.public_materials.all()
    for material in materials:
        if material["id"] == material_id:
            table_data = MaterialPart(material, client).table_data
            n, k = __get_nearest_permittivity(table_data, wavelength)[1]
            return n ** 2 - k ** 2
    raise KeyError(f"Material with id {material_id} not found")


def attach_port(project: MosProject, port, x_y, angle=90, wavelength=1.55):
    assert angle in [90, 0]

    cl: MaxOptics = project.__parent__
    get_material_permittivity = partial(
        __get_material_permittivity, cl, wavelength=wavelength
    )
    # get the region with the highest permittivity
    max_permittivity = 0
    _polygon_with_max_permittivity = None
    polygon_with_max_permittivity = None
    for polygon in project.polygons:
        _polygon = compromised_transform(polygon)
        if x_y in _polygon:
            this_material_permittivity = get_material_permittivity(
                polygon["materialId"]
            )

            if this_material_permittivity > max_permittivity:
                max_permittivity = this_material_permittivity
                _polygon_with_max_permittivity = _polygon
                polygon_with_max_permittivity = polygon

    if not _polygon_with_max_permittivity:
        raise KeyError("Point out of range.")

    crosses = []
    v_x_y = np.array(x_y)

    line = Line(x_y, angle / 180 * pi)

    for segment in _polygon_with_max_permittivity.segments:
        cross = line & segment
        if cross:
            crosses.append(cross)

    min_positive_delta_abs = inf
    min_negative_delta_abs = inf
    positive_pos = deepcopy(x_y)
    negative_pos = deepcopy(x_y)

    for cross in crosses:
        v_cross = np.array(cross)
        delta_v = v_cross - v_x_y
        complex_delta = complex(*delta_v)
        if complex_delta:
            delta_angle = np.angle(complex_delta, deg=True)
            delta_direction = (round(delta_angle - angle) % 360) / 180
            delta_abs = np.abs(complex_delta)
            if not delta_direction:
                if delta_abs < min_positive_delta_abs:
                    min_positive_delta_abs = delta_abs
                    positive_pos = cross
            else:
                if delta_abs < min_negative_delta_abs:
                    min_negative_delta_abs = delta_abs
                    negative_pos = cross

    if positive_pos == x_y and negative_pos == x_y:
        raise ValueError("Can't attach; Structure not found at " + str(x_y))

    port["x_max"] = max(positive_pos[0], negative_pos[0]) + 1
    port["x_min"] = min(positive_pos[0], negative_pos[0]) - 1
    port["y_max"] = max(positive_pos[1], negative_pos[1]) + 1
    port["y_min"] = min(positive_pos[1], negative_pos[1]) - 1
    port["z_max"] = polygon_with_max_permittivity["z_max"]
    port["z_min"] = polygon_with_max_permittivity["z_min"]

    if angle == 90:
        port["x_max"] = x_y[0]
        port["x_min"] = x_y[0]
    elif angle == 0:
        port["y_max"] = x_y[1]
        port["y_min"] = x_y[1]
