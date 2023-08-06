# coding=utf-8
"""This module records the configs"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from attr import define, field, asdict
import yaml

from maxoptics import __ConfigPath__

BASEDIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
__ConfigPath__ = Path(__ConfigPath__)


@define(slots=False, frozen=False)
class ConfigFactory:
    """Configuration for runtime parameters.

    ServerHost is default as None.
    """

    ServerHost: str = None
    ServerPort: int = 80
    OutputDir: Path = field(
        validator=lambda instance, attribute, value: value or ".",
        converter=Path,
        default=__ConfigPath__.parent / "outputs",
    )
    DefaultUser: str = ""
    DefaultPassword: str = field(converter=str, default="")

    SocketPort: int = 80

    # Preference
    Beta: bool = False
    Debug: bool = False
    Verbose: bool = False
    Color: bool = False
    TestOctopusRefactor: bool = False

    # Sometimes things just don't go their way
    ListenSocket: bool = True
    CompatLocalSDK: bool = False
    Login: bool = True
    DisableConstraints: bool = False

    # Base
    DragonURLTemplate: str = "http://{ServerHost}:{ServerPort}/api/%s/"
    WhaleURLTemplate: str = "http://{ServerHost}:{ServerPort}/whale/api/%s/"
    OctopusSIOTemplate: str = "http://{ServerHost}:{SocketPort}"

    # format Pattern
    DefaultLogFolderTemplate: str = "."
    TaskLogFileTemplate: str = "{log_folder}/{project.name}_{task.task_type}_{task.id}/log/terminal.log"

    # Private
    Token: str = ""
    OfflineCompat = False
    __from_MosLibrary__ = False
    __print_level__ = 0

    def update(self, **kwargs):
        new_attributes = {**asdict(self), **kwargs}
        return ConfigFactory(**new_attributes)

    def asdict(self):
        return asdict(self)


@lru_cache(maxsize=1)
def read_config():
    def compat_keys(config_key: str):
        mapping = {
            "SERVERAPI": "ServerHost",
            "SERVERPORT": "ServerPort",
            "OUTPUTDIR": "OutputDir",
            "DEFAULTUSER": "DefaultUser",
            "DEFAULTPASSWORD": "DefaultPassword",
        }
        if config_key.upper() == config_key:
            if config_key in mapping:
                return mapping[config_key]
            elif len(config_key) > 1:
                return config_key[0] + (config_key[1:]).lower()
            else:
                return config_key
        else:
            return config_key

    ret = {}
    if __ConfigPath__.name:
        f = open(__ConfigPath__)
        try:
            user_config = yaml.load(f, yaml.SafeLoader)
            for key in user_config:
                real_key = compat_keys(key)
                val = user_config[key]
                ret[real_key] = val

        except yaml.YAMLError as e:
            print("maxoptics.conf is corrupted! Please check it")
            print(e)
            exit(1)

        f.close()
    return ret


config_dict = read_config()
Config = ConfigFactory(**config_dict)
