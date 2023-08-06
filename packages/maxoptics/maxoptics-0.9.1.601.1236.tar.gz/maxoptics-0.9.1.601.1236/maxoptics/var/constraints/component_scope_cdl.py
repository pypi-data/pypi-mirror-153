from maxoptics.macros import Macro, get_namespace
from maxoptics.var.constraints.component_checks import get_monitor_type

ret = [
    # Affected, Functor{...affectors}
    # X
    ("x", lambda _, x_min, x_max: (float(x_min) + float(x_max)) / 2),
    ("x_span", lambda _, x_min, x_max: float(x_max) - float(x_min)),
    ("x_min", lambda _, x, x_span: float(x) - float(x_span) / 2),
    ("x_max", lambda _, x, x_span: float(x) + float(x_span) / 2),
    ("rotateX", lambda _, rotate_x: 0),
    # Y
    ("y", lambda _, y_min, y_max: (float(y_min) + float(y_max)) / 2),
    ("y_span", lambda _, y_min, y_max: float(y_max) - float(y_min)),
    ("y_min", lambda _, y, y_span: float(y) - float(y_span) / 2),
    ("y_max", lambda _, y, y_span: float(y) + float(y_span) / 2),
    ("rotateY", lambda _, rotate_y: 0),
    # Z
    ("z", lambda _, z_min, z_max: (float(z_min) + float(z_max)) / 2),
    ("z_span", lambda _, z_min, z_max: float(z_max) - float(z_min)),
    ("z_min", lambda _, z, z_span: float(z) - float(z_span) / 2),
    ("z_max", lambda _, z, z_span: float(z) + float(z_span) / 2),
    ("rotateZ", lambda _, rotate_z: 0),
    # Solver
    (
        "mesh_cells_x",
        (
            lambda _, solver_type, mesh_cells_x: 0
            if solver_type in Macro("X_Normal")(get_namespace("FDEAttrs"))
            else (mesh_cells_x or 50)
        ),
    ),
    (
        "mesh_cells_y",
        (
            lambda _, solver_type, mesh_cells_y: 0
            if solver_type in Macro("Y_Normal")(get_namespace("FDEAttrs"))
            else (mesh_cells_y or 50)
        ),
    ),
    (
        "mesh_cells_z",
        (
            lambda _, solver_type, mesh_cells_z: 0
            if solver_type in Macro("Z_Normal")(get_namespace("FDEAttrs"))
            else (mesh_cells_z or 50)
        ),
    ),
    (
        "x_span",
        (
            lambda _, solver_type, x_span: 0
            if solver_type in Macro("X_Normal")(get_namespace("FDEAttrs"))
            else x_span
        ),
    ),
    (
        "y_span",
        (
            lambda _, solver_type, y_span: 0
            if solver_type in Macro("Y_Normal")(get_namespace("FDEAttrs"))
            else y_span
        ),
    ),
    (
        "z_span",
        (
            lambda _, solver_type, z_span: 0
            if solver_type in Macro("Z_Normal")(get_namespace("FDEAttrs"))
            else z_span
        ),
    ),
    # (
    #     "dx",
    #     (
    #         lambda _, x_span, mesh_cells_x: 0.02
    #         if mesh_cells_x == 0
    #         else x_span / mesh_cells_x
    #     ),
    # ),
    # (
    #     "dy",
    #     (
    #         lambda _, y_span, mesh_cells_y: 0.02
    #         if mesh_cells_y == 0
    #         else y_span / mesh_cells_y
    #     ),
    # ),
    # (
    #     "dz",
    #     (
    #         lambda _, z_span, mesh_cells_z: 0.02
    #         if mesh_cells_z == 0
    #         else z_span / mesh_cells_z
    #     ),
    # ),
    # Port
    # EME
    # (
    #     "", lambda _, port_location: pr().emit(_.__parent_ref__(), "EMEPortSetPortLocation", _)
    # ),
    (
        "interval",
        lambda _, start, stop, number_of_points: start - stop
        if number_of_points <= 2
        else (start - stop) / number_of_points,
    ),
    # Others
    ("frequency", lambda _, wavelength: 299792458 / 1000000 / wavelength),
    ("wavelength", lambda _, frequency: 299792458 / 1000000 / frequency),
    (
        "start_frequency",
        lambda _, stop_wavelength: 299792458 / 1000000 / stop_wavelength,
    ),
    (
        "stop_wavelength",
        lambda _, start_frequency: 299792458 / 1000000 / start_frequency,
    ),
    (
        "start_wavelength",
        lambda _, stop_frequency: 299792458 / 1000000 / stop_frequency,
    ),
    (
        "stop_frequency",
        lambda _, start_wavelength: 299792458 / 1000000 / start_wavelength,
    ),
    # Another wavelength repr
    (
        "frequency_min",
        lambda _, wavelength_max: 299792458 / 1000000 / wavelength_max,
    ),
    (
        "wavelength_max",
        lambda _, frequency_min: 299792458 / 1000000 / frequency_min,
    ),
    (
        "wavelength_min",
        lambda _, frequency_max: 299792458 / 1000000 / frequency_max,
    ),
    (
        "frequency_max",
        lambda _, wavelength_min: 299792458 / 1000000 / wavelength_min,
    ),
    #
    (
        "wavelength_span",
        lambda _, wavelength_min, wavelength_max: wavelength_max
        - wavelength_min,
    ),
    (
        "wavelength_center",
        lambda _, wavelength_min, wavelength_max: (
            wavelength_min + wavelength_max
        )
        / 2,
    ),
    (
        "frequency_span",
        lambda _, frequency_min, frequency_max: frequency_max - frequency_min,
    ),
    (
        "frequency_center",
        lambda _, frequency_min, frequency_max: (frequency_min + frequency_max)
        / 2,
    ),
    #
    (
        "wavelength_min",
        lambda _, wavelength_center, wavelength_span: wavelength_center
        - wavelength_span / 2,
    ),
    (
        "wavelength_max",
        lambda _, wavelength_center, wavelength_span: wavelength_center
        + wavelength_span / 2,
    ),
    (
        "frequency_min",
        lambda _, frequency_center, frequency_span: frequency_center
        - frequency_span / 2,
    ),
    (
        "frequency_max",
        lambda _, frequency_center, frequency_span: frequency_center
        + frequency_span / 2,
    ),
    ("h", lambda _, z_span: float(z_span)),
    ("bent_radius", lambda _, bend_radius: bend_radius),
    ("bend_radius", lambda _, bent_radius: bent_radius),
    (
        "overrideMeshOrder",
        lambda _, meshOrder: 0 if meshOrder == -1 else 1,
    ),
    # monitor_type
    (
        "monitor_type",
        lambda _, x_span, y_span, z_span, monitor_type: get_monitor_type(
            x_span, y_span, z_span
        ),
    ),
    # fix holes
    ("modeindex", lambda _, mode_index: mode_index),
    ("modeIndex", lambda _, mode_index: mode_index),
]
