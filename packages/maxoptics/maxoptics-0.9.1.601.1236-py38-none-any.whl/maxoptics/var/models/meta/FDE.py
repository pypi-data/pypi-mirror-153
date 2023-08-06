# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Solver
from weakref import ref

__all__ = ("FDE",)


class FDE(Solver):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = FDEActions(component_ref)
        self.attrs = FDEAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconMODE"
        self.id = ""
        self.locked = False
        self.name = "FDE"
        self.order = 1
        self.order = "0"
        self.tabs = [
            "General",
            "Geometry",
            "Mesh settings",
            "Boundary conditions",
            "Material",
        ]
        self.type = FDEType(component_ref)
        self.__belong2__ = {"active": ["Document"], "passive": ["Document"]}
        super().__init__(project_ref)


class FDEActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class FDEAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.actual_mesh_cells_x = 0
        self.actual_mesh_cells_y = 0
        self.actual_mesh_cells_z = 0
        self.background_material = "P41"
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.define_x_mesh = 1
        self.define_y_mesh = 1
        self.define_z_mesh = 1
        self.detailed_dispersion_calculation = 1
        self.dxd = 0.02
        self.dyd = 0.02
        self.dzd = 0.02
        self.effective_index = 1
        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.force_symmetric_x_mesh = 0
        self.force_symmetric_y_mesh = 0
        self.force_symmetric_z_mesh = 0
        self.frequency = 193.414
        self.grading_factor = 1.2
        self.index = 1.4
        self.mesh_cells_x = 50
        self.mesh_cells_y = 50
        self.mesh_cells_z = 0
        self.meshing_refinement = 0
        self.min_mesh_step = 0.0001
        self.n = 1
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.pml_kappa = 1
        self.pml_layers = 10
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.refinement_type = 1
        self.search = 1
        self.simulation_temperature = 300
        self.solver_type = 0
        self.spatial = FDEAttrsSpatial(component_ref)
        self.start_frequency = 193.414
        self.start_wavelength = 1.55
        self.stop_frequency = 200
        self.stop_wavelength = 1.49896
        self.store_mode_profiles_while_tracking = 0
        self.track_selected_mode = 0
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x = 0
        self.x_max = 0
        self.x_max_bc = 1
        self.x_min = 0
        self.x_min_bc = 1
        self.x_span = 3
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
        self.z_span = 0

        super().__init__(component_ref)


class FDEAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDEType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FDETypeActions(component_ref)
        self.attrs = FDETypeAttrs(component_ref)
        self.base = FDETypeBase(component_ref)
        self.icon = "iconMODE"
        self.name = "FDE"
        self.order = "0"
        self.tabs = [
            "General",
            "Geometry",
            "Mesh settings",
            "Boundary conditions",
            "Material",
        ]

        super().__init__(component_ref)


class FDETypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        super().__init__(component_ref)


class FDETypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actual_mesh_cells_x = 0
        self.actual_mesh_cells_y = 0
        self.actual_mesh_cells_z = 0
        self.background_material = "P41"
        self.bend_location = 0
        self.bend_orientation = 0
        self.bend_radius = 1
        self.bent_waveguide = 0
        self.calculate_group_index = 0
        self.define_x_mesh = 1
        self.define_y_mesh = 1
        self.define_z_mesh = 1
        self.detailed_dispersion_calculation = 1
        self.dxd = 0.02
        self.dyd = 0.02
        self.dzd = 0.02
        self.effective_index = 1
        self.expre_x = ""
        self.expre_x_max = ""
        self.expre_x_min = ""
        self.expre_x_span = ""
        self.expre_y = ""
        self.expre_y_max = ""
        self.expre_y_min = ""
        self.expre_y_span = ""
        self.expre_z = ""
        self.expre_z_max = ""
        self.expre_z_min = ""
        self.expre_z_span = ""
        self.force_symmetric_x_mesh = 0
        self.force_symmetric_y_mesh = 0
        self.force_symmetric_z_mesh = 0
        self.frequency = 193.414
        self.grading_factor = 1.2
        self.index = 1.4
        self.mesh_cells_x = 50
        self.mesh_cells_y = 50
        self.mesh_cells_z = 0
        self.meshing_refinement = 0
        self.min_mesh_step = 0.0001
        self.n = 1
        self.number_of_points = 10
        self.number_of_test_modes = 3
        self.number_of_trial_modes = 20
        self.pml_kappa = 1
        self.pml_layers = 10
        self.pml_polynomial = 3
        self.pml_sigma = 5
        self.refinement_type = 1
        self.search = 1
        self.simulation_temperature = 300
        self.solver_type = 2
        self.spatial = FDETypeAttrsSpatial(component_ref)
        self.start_frequency = 193.414
        self.start_wavelength = 1.55
        self.stop_frequency = 200
        self.stop_wavelength = 1.49896
        self.store_mode_profiles_while_tracking = 0
        self.track_selected_mode = 0
        self.use_max_index = 1
        self.wavelength = 1.55
        self.x = 0
        self.x_max = 1.5
        self.x_max_bc = 1
        self.x_min = 1.5
        self.x_min_bc = 1
        self.x_span = 3
        self.y = 0
        self.y_max = 1.5
        self.y_max_bc = 1
        self.y_min = -1.5
        self.y_min_bc = 1
        self.y_span = 3
        self.z = 0
        self.z_max = 0
        self.z_max_bc = 1
        self.z_min = 0
        self.z_min_bc = 1
        self.z_span = 0

        super().__init__(component_ref)


class FDETypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDETypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FDETypeBaseActions(component_ref)
        self.attrs = FDETypeBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "ArithmeticObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FDETypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.disable = "disable"
        self.edit = "edit"
        self.remove = "remove"

        super().__init__(component_ref)


class FDETypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = FDETypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class FDETypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)
