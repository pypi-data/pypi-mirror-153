import weakref

from maxoptics.core.base.BaseContainer import (
    BaseSearchContainer,
    MaterialShell,
    WaveformShell,
)


class PublicMaterials(BaseSearchContainer[MaterialShell]):
    """Handle public materials."""

    def __init__(self, mos):
        super().__init__()
        self.project_type = "passive"
        self.mos = mos

    def reload(self):
        """Load public materials from server"""
        data = self.mos.post(url="get_public_materials", token=self.mos.token)[
            "result"
        ]["public_materials"]

        self._cached = [MaterialShell(_) for _ in data]

    def __getitem__(self, keyval: str):
        return self.all()[self._get_index(keyval=keyval)]

    def __setitem__(self, keyval: str, val):
        raise NotImplementedError("Disallow to change public material")


class UserMaterials(BaseSearchContainer[MaterialShell]):
    """Handle materials."""

    def __init__(self, mos, project_type):
        super().__init__()
        self.mos = mos
        self.project_type = project_type
        self.deleter = weakref.WeakMethod(mos.delete_material)

    def reload(self):
        """Load materials from server"""
        data = self.mos.post(
            url="search_materials",
            token=self.mos.token,
            project_type=self.project_type,
        )["result"]["result"]

        self._cached = [MaterialShell(_) for _ in data]

    def __getitem__(self, keyval: str):
        return self.all()[self._get_index(keyval=keyval)]

    def __setitem__(self, keyval: str, val):
        raise NotImplementedError()


class UserWaveforms(BaseSearchContainer[WaveformShell]):
    """Handle waveforms."""

    def __init__(self, mos):
        super().__init__()
        self.mos = mos
        self.deleter = weakref.WeakMethod(mos.delete_waveform)

    def reload(self):
        """Load waveforms from server"""
        ret = self.mos.post(url="search_waveforms", token=self.mos.token)[
            "result"
        ]
        data = ret["result"]

        self._cached = [WaveformShell(_) for _ in data]

    def __getitem__(self, keyval: str):
        return self.all()[self._get_index(keyval=keyval)]

    def __setitem__(self, keyval: str, val):
        raise NotImplementedError()
