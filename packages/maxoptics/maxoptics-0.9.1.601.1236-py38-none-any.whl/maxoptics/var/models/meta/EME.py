# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Solver
from weakref import ref

__all__ = ("EME",)


class EME(Solver):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = EMEActions(component_ref)
        self.attrs = EMEAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconEME"
        self.id = ""
        self.locked = False
        self.name = "EME"
        self.order = 3
        self.order = "0"
        self.tabs = [
            "General",
            "EME Setup",
            "Transverse mesh settings",
            "Boundary conditions",
            "Material",
            "Advanced options",
        ]
        self.type = EMEType(component_ref)
        self.__belong2__ = {"passive": ["Document", "*"]}
        super().__init__(project_ref)


class EMEActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EMEAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.actual_mesh_cells_x = 0
        self.actual_mesh_cells_y = 0
        self.actual_mesh_cells_z = 0
        self.algorithm = 0
        self.allow_symmetry = True
        self.amplitude = 1
        self.background_material = "P41"
        self.calculate_group_delays = 0
        self.cell_group = []
        self.convergence_tolerance = 1e-12
        self.define_x_mesh = 1
        self.define_y_mesh = 1
        self.define_z_mesh = 1
        self.display_cells = 0
        self.dx = 0.02
        self.dy_arr = [0]
        self.dy = 0.02
        self.dy_arr = self.__lazy_attr__(lambda _: [_.dy] * _.mesh_cells_y)
        self.dz = 0.02
        self.dz_arr = self.__lazy_attr__(lambda _: [_.dz] * _.mesh_cells_z)

        self.energy_conversation = 1
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.frequency = 193.414
        self.grading_factor = 1.2
        self.group_delay = 0.0001
        self.index = 1.4
        self.interval = 0
        self.max_stored_modes = 1000
        self.mesh_cells_x = 0
        self.mesh_cells_y = 50
        self.mesh_cells_z = 50
        self.meshing_refinement = 0
        self.min_mesh_step = 1e-05
        self.number_of_points = 2
        self.number_of_wavelength_points = 2
        self.originGeometry = {}
        self.parameter = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.propagation = 1
        self.refinement_type = 1
        self.simulation_temperature = 300
        self.solver_type = 0
        self.source_mode = 0
        self.source_port = 0
        self.spatial = EMEAttrsSpatial(component_ref)
        self.start = 0
        self.start_wavelength = 1.5
        self.stop = 0
        self.stop_wavelength = 1.6
        self.use_wavelength_sweep = 1
        self.wavelength = 1.55
        self.x = 0
        self.x_max = 5
        self.x_max_bc = 0
        self.x_min = -5
        self.x_min_bc = 0
        self.x_span = 10
        self.y = 0
        self.y_max = 0
        self.y_max_bc = 1
        self.y_min = 0
        self.y_min_bc = 1
        self.y_span = 3
        self.z = 0
        self.z_max = 0
        self.z_max_bc = 1
        self.z_min = 0
        self.z_min_bc = 1
        self.z_span = 3

        super().__init__(component_ref)


class EMEAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EMEType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EMETypeActions(component_ref)
        self.attrs = EMETypeAttrs(component_ref)
        self.base = EMETypeBase(component_ref)
        self.icon = "iconEME"
        self.name = "EME"
        self.order = "0"
        self.tabs = [
            "General",
            "EME Setup",
            "Transverse mesh settings",
            "Boundary conditions",
            "Material",
            "Advanced options",
        ]

        super().__init__(component_ref)


class EMETypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class EMETypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actual_mesh_cells_x = 0
        self.actual_mesh_cells_y = 0
        self.actual_mesh_cells_z = 0
        self.algorithm = 0
        self.allow_symmetry = True
        self.amplitude = 1
        self.background_material = "P41"
        self.calculate_group_delays = 0
        self.cell_group = [
            {"cell_num": 5, "number_of_modes": 10, "sc": 0, "span": 10}
        ]
        self.convergence_tolerance = 1e-12
        self.define_x_mesh = 1
        self.define_y_mesh = 1
        self.define_z_mesh = 1
        self.display_cells = 0
        self.dx = 0.02
        self.dy = 0.02
        self.dz = 0.02
        self.energy_conversation = 1
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.frequency = 193.414
        self.grading_factor = 1.2
        self.group_delay = 0.0001
        self.index = 1.4
        self.interval = 0
        self.max_stored_modes = 1000
        self.mesh_cells_x = 0
        self.mesh_cells_y = 50
        self.mesh_cells_z = 50
        self.meshing_refinement = 0
        self.min_mesh_step = 1e-05
        self.number_of_points = 2
        self.number_of_wavelength_points = 2
        self.parameter = 0
        self.pml_kappa = 2
        self.pml_layers = 12
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.propagation = 1
        self.refinement_type = 1
        self.simulation_temperature = 300
        self.solver_type = 0
        self.source_mode = 0
        self.source_port = 0
        self.spatial = EMETypeAttrsSpatial(component_ref)
        self.start = 0
        self.start_wavelength = 1.5
        self.stop = 0
        self.stop_wavelength = 1.6
        self.use_wavelength_sweep = 1
        self.wavelength = 1.55
        self.x = 0
        self.x_max = 5
        self.x_max_bc = 0
        self.x_min = -5
        self.x_min_bc = 0
        self.x_span = 10
        self.y = 0
        self.y_max = 0
        self.y_max_bc = 1
        self.y_min = 0
        self.y_min_bc = 1
        self.y_span = 3
        self.z = 0
        self.z_max = 0
        self.z_max_bc = 1
        self.z_min = 0
        self.z_min_bc = 1
        self.z_span = 3

        super().__init__(component_ref)


class EMETypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class EMETypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = EMETypeBaseActions(component_ref)
        self.attrs = EMETypeBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "ArithmeticObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class EMETypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.disable = "disable"
        self.edit = "edit"
        self.remove = "remove"

        super().__init__(component_ref)


class EMETypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = EMETypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class EMETypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)
