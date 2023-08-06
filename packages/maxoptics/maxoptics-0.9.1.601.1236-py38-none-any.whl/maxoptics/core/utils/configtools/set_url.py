import json
import os
import tkinter as tk
from pathlib import Path

import requests
import yaml
from yaml.error import YAMLError

BASEDIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def set_url():
    def inputurl():
        nonlocal url
        try:
            url = str(var.get().strip())
            res1 = False
            res2 = False
            var2.set("Connecting")
            res1 = requests.post(
                "{}/api/ping/".format(url[:-1] if url[-1] == "/" else url),
                data=json.dumps({}),
                headers={
                    "Content-Type": "application/json",
                    "Connection": "close",
                },
            )
            res2 = requests.post(
                "{}/whale/api/get_mode_solver_result/".format(
                    url[:-1] if url[-1] == "/" else url
                ),
                data=json.dumps({}),
                headers={
                    "Content-Type": "application/json",
                    "Connection": "close",
                },
            )
            if (
                res1
                and res2
                and res1.status_code == 200
                and res2.status_code == 200
            ):
                url = url.replace("https://", "").replace("http://", "")
                if "default.conf" in os.listdir(BASEDIR):
                    with open(BASEDIR / "default.conf", "r") as f:
                        try:
                            conf = yaml.load(f, yaml.BaseLoader)
                        except YAMLError:
                            conf = {}
                else:
                    conf = {}
                conf.update({"ServerHost": url})
                with open(BASEDIR / "default.conf", "w") as f:
                    f.write(yaml.dump(conf))
            else:
                raise ValueError
        except Exception:
            var.set("http://")
            var2.set("Invalid url")

    def inputcancel():
        exit()

    url: str = ""
    root = tk.Tk(className="Please input url")
    root.geometry("270x100+750+200")

    var = tk.StringVar()
    var.set("http://")
    entry1 = tk.Entry(root, textvariable=var)
    entry1.pack()

    var2 = tk.StringVar()
    var2.set("Please input url")
    entry2 = tk.Entry(root, textvariable=var2, state="disabled", fg="red")
    entry2.pack()
    btn1 = tk.Button(root, text="Confirm", command=inputurl)
    btn2 = tk.Button(root, text="Cancel", command=inputcancel)

    btn2.pack(side="right")
    btn1.pack(side="right")

    root.mainloop()


if __name__ == "__main__":
    set_url()
