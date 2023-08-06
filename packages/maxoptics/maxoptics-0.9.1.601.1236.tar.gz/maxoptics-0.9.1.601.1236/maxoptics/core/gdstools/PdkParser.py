import os
import re


class LayerDesc:
    def __init__(self, name):
        self.name = name or ""
        self.id = 0  # GDSII layer number
        self.datatype = 0  # GDSII layer data type
        self.height = 0  # Start height (usually in nm)
        self.thickness = 0  # Thickness (usually in nm)
        self.color_r = 0  # Red color component (0.0-1.0)
        self.color_g = 0  # Green color component (0.0-1.0)
        self.color_b = 0  # Blue color component (0.0-1.0)
        self.alpha = 0  # Transparency (do not use)
        self.meshOrder = 0  # Mesh render order
        self.mateType = ""  # material type
        self.show = 0  # Set to 0 for layers that are not to be rendered
        self.freeze = 0  # disabled change attr

    def hexColor(self):
        return


class PdkDesc:
    def __init__(self):
        self.layers = {}

    def adjust_unit(self, unit, precision):
        """
        调整单位: PDK中是以nm为单位, GDS是μm为单位;
        """

        unit_r = 1e-09 / unit
        prec_r = round(unit / precision)
        if unit_r > 0.5:
            unit_r = round(unit_r)
        self.__adjust(unit_r, prec_r)

    def __adjust(self, unit_r=1.0, prec_r=1.0):
        if unit_r == 1.0:
            return
        for l in self.layers.values():
            l.height *= unit_r
            l.thickness *= unit_r


class PdkParser:
    @classmethod
    def load(self, filename) -> PdkDesc:
        """
        载入pdf的描述信息
        """
        if not os.path.exists(filename):
            return None
        lines = open(filename).readlines()
        if len(lines) == 0:
            return None

        desc = PdkDesc()
        layer = None
        for line in lines:
            key, value = self.__getKeyValue(line)
            if (key is None) or (len(key) == 0):
                continue
            if self.__isSame(key, "LayerStart"):
                layer = LayerDesc(value)
            elif self.__isSame(key, "Layer"):
                layer.id = int(value)
            elif self.__isSame(key, "datatype"):
                layer.datatype = int(value)
            elif self.__isSame(key, "Height"):
                layer.height = int(value)
            elif self.__isSame(key, "Thickness"):
                layer.thickness = int(value)
            elif self.__isSame(key, "Red"):
                layer.color_r = float(value)
            elif self.__isSame(key, "Green"):
                layer.color_g = float(value)
            elif self.__isSame(key, "Blue"):
                layer.color_b = float(value)
            elif self.__isSame(key, "alpha"):
                layer.alpha = float(value)
            elif self.__isSame(key, "MeshOrder"):
                layer.meshOrder = int(value)
            elif self.__isSame(key, "MateType"):
                layer.mateType = value
            elif self.__isSame(key, "Show"):
                layer.show = int(value)
            elif self.__isSame(key, "Freeze"):
                layer.show = int(value)
            elif self.__isSame(key, "LayerEnd"):
                desc.layers[tuple([layer.id, layer.datatype])] = layer
                layer = None

        return desc

    @classmethod
    def __getKeyValue(self, line):
        key = value = None
        temp = re.compile("#[\s\S]*$").sub("", line)
        if line.find(":") >= 0:
            list = temp.split(":")
            key = list[0].strip()
            value = list[1].strip()
        else:
            key = temp.strip()
        return [key, value]

    @classmethod
    def __isSame(self, v1, v2) -> bool:
        return v1.upper() == v2.upper()
