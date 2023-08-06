import os
from pathlib import Path

import yaml

BASEDIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def set_value(name, value):
    if "default.conf" in os.listdir(BASEDIR):
        with open(BASEDIR / "default.conf", "r") as f:
            try:
                conf = yaml.load(f, yaml.BaseLoader)
            except yaml.YAMLError:
                conf = {}
    else:
        conf = {}

    conf.update({name: value})
    with open(BASEDIR / "default.conf", "w") as f:
        f.write(yaml.dump(conf))
