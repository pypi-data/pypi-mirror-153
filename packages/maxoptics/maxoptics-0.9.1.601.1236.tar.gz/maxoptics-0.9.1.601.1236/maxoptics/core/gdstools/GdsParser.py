from typing import List

import gdspy

from maxoptics.core.logger import (
    error_print,
    info_print,
    warn_print,
)
from .GdsMaterial import GdsMaterial
from .ProgressBar import ProgressBar
from .structures import Structure
from ..error import ProjectBuildError


class GdsModel(object):
    def __init__(self, project, sdk):
        self.project = project
        self.sdk = sdk

    def gds_import(
        self, gdsfile, cellname, layer, material, zmin, zmax
    ) -> List[object]:
        """
        导入GDSII 文件
        """
        layer_id, datatype = layer.split("/")
        layer_key = tuple([int(layer_id), int(datatype)])

        # 这个版本暂时先不使用Techfile描述文件
        # # 0. 载入PDK 的 Layer描述信息
        # pdk =  PdkParser.load(techfile)
        # if pdk is None:
        #     error_print("读取PDK描述信息失败: %s" % techfile)
        #     return

        # if layer_key not in pdk.layers:
        #     info_print("PDK中没有关于这个层的描述: %s/%s" % (layer_id, datatype))
        #     return

        # 1. 载入GDS文件, 获取要处理的cells和polygons
        library = gdspy.GdsLibrary(infile=gdsfile)
        if library is None:
            error_print("import GDS file failed. GDS File: %s" % gdsfile)
            raise ProjectBuildError(
                "GdsPolygon", "import GDS file failed. GDS File: %s" % gdsfile
            )

        cells = dict(library.cells)
        if (len(cells) == 0) or (cellname not in cells.keys()):
            warn_print("cell not  found. cellName: %s" % cellname)
            raise ProjectBuildError(
                "GdsPolygon", "cell not  found. cellName: %s" % cellname
            )

        cell_polygons = cells[cellname].get_polygons(True, None)
        if layer_key not in cell_polygons:
            warn_print(f"layer not found. layerKey: {layer_key}")
            raise ProjectBuildError(
                "GdsPolygon", f"layer not found. layerKey: {layer_key}"
            )

        # arr_polygon = [pol for pol in cell_polygons if (int(layerid) in pol.layers) and (int(datatype) in
        # pol.datatypes)]
        arr_polygon = cell_polygons[layer_key]
        if len(arr_polygon) == 0:
            warn_print(f"polygon not found. layerKey: {layer_key}")
            raise ProjectBuildError(
                "GdsPolygon", f"polygon not found. layerKey: {layer_key}"
            )

        # 这个版本暂时先不使用Techfile描述文件
        # 2. 统一PDK 和 GDS 的数值单位
        # pdk.adjust_unit(library.unit, library.precision)
        # layer_desc = pdk.layers[layer_key]
        layer_desc = {"z": zmin, "h": zmax - zmin, "zmin": zmin, "zmax": zmax}

        # 3. 获取对应的Material信息, 如果不存在则新增;
        materialObj = GdsMaterial.getByInfo(self.sdk, material)
        if len(materialObj) <= 0:
            warn_print(f"material not found. key: {material}")
            raise ProjectBuildError(
                "GdsPolygon", f"material not found. key: {material}"
            )

        # 4. 将这些cells和polygons加入项目
        objs = []
        progress = ProgressBar(iteration=0, total=len(arr_polygon), length=50)
        for idx, polygon in enumerate(arr_polygon):
            obj = Structure.addToProject(
                idx, polygon, materialObj, layer_desc, self.project
            )
            objs.append(obj)
            progress.walk()

        info_print("GDS import Success!\n")
        return objs

    def gen_polygon(self, points):
        """
        根据给定的点数组生成多边形，并加入Project:
        points: 逆时针是实体, 顺时针是孔洞;
        """
        return Structure.addToProject(
            len(self.project.components), points, None, None, self.project
        )
