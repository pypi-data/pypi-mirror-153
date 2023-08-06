from typing import Any
from typing import Mapping

import pandas as pd

from maxoptics.core.base.BaseContainer import MaterialShell


class GdsMaterial:
    @classmethod
    def getByInfo(self, sdk, info) -> Any:
        if isinstance(info, Mapping):
            return self.getById(sdk, info["id"])
        elif isinstance(info, MaterialShell):
            return self.getById(sdk, info.id)
        elif isinstance(info, int):
            return self.getById(sdk, info)
        elif isinstance(info, str):
            if info[0] == "P" and info[1:].isdigit():
                return self.getById(sdk, info)
            else:
                return self.getByName(sdk, info)
        return self.getByName(sdk, info)

    @classmethod
    def getById(self, sdk, id) -> Any:
        self.__initSDK(sdk)
        return self.materials.loc[self.materials.id == id]

    @classmethod
    def getByName(self, sdk, name) -> Any:
        self.__initSDK(sdk)
        return self.materials.loc[self.materials.name == name]

    @classmethod
    def getByPdkDesc(self, sdk, layer_desc) -> Any:
        self.__initSDK(sdk)
        return self.__matchMaterial(layer_desc)

    @classmethod
    def __initSDK(self, sdk):
        if not hasattr(self, "materials"):
            self.sdk = sdk
            materials_raw_pub = self.sdk.public_materials.all()
            materials_raw_user = self.sdk.user_materials.all()
            materials_raw = materials_raw_pub + materials_raw_user
            self.materials = pd.DataFrame(materials_raw)

    @classmethod
    def __matchMaterial(self, layer_desc):
        name = "gds material %d" % len(self.materials)
        color = self.__hexColor(
            layer_desc.color_r, layer_desc.color_g, layer_desc.color_b
        )
        type = layer_desc.mateType
        temperature = 0
        mesh_order = layer_desc.meshOrder
        data = {"rel_permitivity": 12.666481}

        # 根据属性信息匹配相近的
        df = self.materials
        mat = df.loc[
            (df["color"] == color)
            & (df["type"] == type)
            & (df["mesh_order"] == mesh_order)
            & (df["rel_permitivity"] == data["rel_permitivity"])
        ]
        if len(mat) > 0:
            return mat

        # 创建个新的
        mat = self.sdk.create_material(
            name, color, type, temperature, mesh_order, data
        )
        return mat

    @classmethod
    def __clamp(self, v):
        return max(0, min(int(v * 255), 255))

    @classmethod
    def __hexColor(self, r, g, b):
        return "{0:02x}{1:02x}{2:02x}".format(
            self.__clamp(r), self.__clamp(g), self.__clamp(b)
        ).upper()
