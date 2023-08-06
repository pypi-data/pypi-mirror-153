# coding=utf-8
from maxoptics.core.component.base.Attrs import ProjectComponentAttrsBase
from maxoptics.core.component.base.Component import Solver
from weakref import ref

__all__ = ("FDTD",)


class FDTD(Solver):
    def __init__(self, project_ref):
        component_ref = ref(self)
        self.actions = FDTDActions(component_ref)
        self.attrs = FDTDAttrs(component_ref)
        self.children = []
        self.disabled = False
        self.icon = "iconsimulation-fdtd"
        self.id = ""
        self.locked = False
        self.name = "FDTD"
        self.order = 2
        self.order = "0"
        self.tabs = [
            "General",
            "Geometry",
            "Mesh settings",
            "Boundary conditions",
            "Advanced options",
            "Thread settings",
        ]
        self.type = FDTDType(component_ref)
        self.__belong2__ = {"active": ["Document"], "passive": ["Document"]}
        super().__init__(project_ref)


class FDTDActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.runFDTD = "runFDTD"

        super().__init__(component_ref)


class FDTDAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self._objLink = []
        self.amp = "amplitude"
        self.auto_shutoff_max = 100000
        self.auto_shutoff_min = 0.0001
        self.background_material = "P41"
        self.bandwidth_config = FDTDAttrsBandwidth_config(component_ref)
        self.cells_per_wavelength = 15
        self.component = "E"
        self.dimension = 1
        self.down_sample_time = 100
        self.dx = 0.1
        self.dx_arr = []
        self.dy = 0.1
        self.dy_arr = []
        self.dz = 0.1
        self.dz_arr = []
        self.estimate_time = 1000
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
        self.extend_structure_through_pml = 1
        self.frequency_scale = False
        self.grading = 1
        self.grading_factor = 1.2
        self.horizontalt = 0
        self.index = 1.4
        self.mesh_type = 0
        self.meshing_refinement = 1
        self.min_mesh_step = 0.0001
        self.plot = 0
        self.plot_with = 0
        self.pml_config = FDTDAttrsPml_config(component_ref)
        self.pml_same_settings = 1
        self.polarized_type = 0
        self.refinement_type = 0
        self.scale = False
        self.set_bandwidth = 0
        self.simulation_temperature = 300
        self.simulation_time = 1000
        self.spatial = FDTDAttrsSpatial(component_ref)
        self.thread = 4
        self.time_stop = 0
        self.use_divergence_checking = 0
        self.use_early_shutoff = 1
        self.using_optical_path_estimate_time = 0
        self.x = 0
        self.x_max = 12
        self.x_max_bc = 0
        self.x_max_pml_config = FDTDAttrsX_max_pml_config(component_ref)
        self.x_min = -12
        self.x_min_bc = 0
        self.x_min_pml_config = FDTDAttrsX_min_pml_config(component_ref)
        self.x_span = 24
        self.y = 0
        self.y_max = 8
        self.y_max_bc = 0
        self.y_max_pml_config = FDTDAttrsY_max_pml_config(component_ref)
        self.y_min = -8
        self.y_min_bc = 0
        self.y_min_pml_config = FDTDAttrsY_min_pml_config(component_ref)
        self.y_span = 16
        self.z = 0
        self.z_max = 5
        self.z_max_bc = 0
        self.z_max_pml_config = FDTDAttrsZ_max_pml_config(component_ref)
        self.z_min = -5
        self.z_min_bc = 0
        self.z_min_pml_config = FDTDAttrsZ_min_pml_config(component_ref)
        self.z_span = 10

        super().__init__(component_ref)


class FDTDAttrsBandwidth_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.center_frequency = 0
        self.center_wavelength = 0
        self.frequency_span = 0
        self.frequency_start = 0
        self.frequency_stop = 0
        self.range_type = 0
        self.type = 0
        self.wavelength_span = 0
        self.wavelength_start = 0
        self.wavelength_stop = 0

        super().__init__(component_ref)


class FDTDAttrsPml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDAttrsX_max_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDAttrsX_min_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDAttrsY_max_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDAttrsY_min_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDAttrsZ_max_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDAttrsZ_min_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDType(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FDTDTypeActions(component_ref)
        self.attrs = FDTDTypeAttrs(component_ref)
        self.base = FDTDTypeBase(component_ref)
        self.icon = "iconsimulation-fdtd"
        self.name = "FDTD"
        self.order = "0"
        self.tabs = [
            "General",
            "Geometry",
            "Mesh settings",
            "Boundary conditions",
            "Advanced options",
            "Thread settings",
        ]

        super().__init__(component_ref)


class FDTDTypeActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.runFDTD = "runFDTD"

        super().__init__(component_ref)


class FDTDTypeAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.amp = "amplitude"
        self.auto_shutoff_max = 100000
        self.auto_shutoff_min = 0.0001
        self.background_material = "P41"
        self.bandwidth_config = FDTDTypeAttrsBandwidth_config(component_ref)
        self.cells_per_wavelength = 15
        self.component = "E"
        self.dimension = 1
        self.down_sample_time = 100
        self.dx = 0.1
        self.dy = 0.1
        self.dz = 0.1
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
        self.extend_structure_through_pml = 1
        self.frequency_scale = False
        self.grading = 1
        self.grading_factor = 1.2
        self.horizontalt = 0
        self.index = 1.4
        self.mesh_type = 0
        self.meshing_refinement = 1
        self.min_mesh_step = 0.0001
        self.plot = 0
        self.plot_with = 0
        self.pml_config = FDTDTypeAttrsPml_config(component_ref)
        self.pml_same_settings = 1
        self.polarized_type = 0
        self.refinement_type = 0
        self.scale = False
        self.set_bandwidth = 0
        self.simulation_temperature = 300
        self.simulation_time = 1000
        self.spatial = FDTDTypeAttrsSpatial(component_ref)
        self.thread = 4
        self.time_stop = 0
        self.use_divergence_checking = 0
        self.use_early_shutoff = 1
        self.x = 0
        self.x_max = 12
        self.x_max_bc = 0
        self.x_max_pml_config = FDTDTypeAttrsX_max_pml_config(component_ref)
        self.x_min = -12
        self.x_min_bc = 0
        self.x_min_pml_config = FDTDTypeAttrsX_min_pml_config(component_ref)
        self.x_span = 24
        self.y = 0
        self.y_max = 8
        self.y_max_bc = 0
        self.y_max_pml_config = FDTDTypeAttrsY_max_pml_config(component_ref)
        self.y_min = -8
        self.y_min_bc = 0
        self.y_min_pml_config = FDTDTypeAttrsY_min_pml_config(component_ref)
        self.y_span = 16
        self.z = 0
        self.z_max = 5
        self.z_max_bc = 0
        self.z_max_pml_config = FDTDTypeAttrsZ_max_pml_config(component_ref)
        self.z_min = -5
        self.z_min_bc = 0
        self.z_min_pml_config = FDTDTypeAttrsZ_min_pml_config(component_ref)
        self.z_span = 10

        super().__init__(component_ref)


class FDTDTypeAttrsBandwidth_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.center_frequency = 0
        self.center_wavelength = 0
        self.frequency_span = 0
        self.frequency_start = 0
        self.frequency_stop = 0
        self.range_type = 0
        self.type = 0
        self.wavelength_span = 0
        self.wavelength_start = 0
        self.wavelength_stop = 0

        super().__init__(component_ref)


class FDTDTypeAttrsPml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDTypeAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)


class FDTDTypeAttrsX_max_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDTypeAttrsX_min_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDTypeAttrsY_max_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDTypeAttrsY_min_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDTypeAttrsZ_max_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDTypeAttrsZ_min_pml_config(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.alpha = 0
        self.alpha_polynomial = 1
        self.kappa = 2
        self.layers = 8
        self.max_layers = 64
        self.min_layers = 8
        self.polynomial = 3
        self.profile = "Standard"
        self.sigma = 1

        super().__init__(component_ref)


class FDTDTypeBase(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.actions = FDTDTypeBaseActions(component_ref)
        self.attrs = FDTDTypeBaseAttrs(component_ref)
        self.icon = "suanfa8"
        self.name = "ArithmeticObject"
        self.order = "0"
        self.tabs = []

        super().__init__(component_ref)


class FDTDTypeBaseActions(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.disable = "disable"
        self.edit = "edit"
        self.remove = "remove"

        super().__init__(component_ref)


class FDTDTypeBaseAttrs(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.spatial = FDTDTypeBaseAttrsSpatial(component_ref)

        super().__init__(component_ref)


class FDTDTypeBaseAttrsSpatial(ProjectComponentAttrsBase):
    def __init__(self, component_ref):

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0
        self.x = 0
        self.y = 0
        self.z = 0

        super().__init__(component_ref)
