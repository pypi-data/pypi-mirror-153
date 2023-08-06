import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import yaml
from yaml.error import YAMLError

BASEDIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def set_save_dir():
    if "default.conf" in os.listdir(BASEDIR):
        with open(BASEDIR / "default.conf", "r") as f:
            try:
                conf = yaml.load(f, yaml.Loader)
            except YAMLError:
                conf = {}
    else:
        conf = {}

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    if not file_path:
        return
    conf.update({"OutputDir": file_path})
    with open(BASEDIR / "default.conf", "w") as f:
        f.write(yaml.dump(conf))


if __name__ == "__main__":
    set_save_dir()
