import inspect
import json
import os
from abc import ABC

import requests

from maxoptics.core.logger import error_print
from maxoptics.core.project.utils import Index
from .BaseClient import BaseClient


class WhaleClients(BaseClient, ABC):
    def __init__(
        self, task_id, project=None, config=None, status=0, tarsrc_name=None
    ):
        super().__init__("WhaleURLTemplate")
        self.task_id = int(task_id)
        self.monitor_num = 0
        self.id = task_id
        self.status = status
        self.project = project
        self.task_type = ""
        self.tarsrc_name = tarsrc_name
        self.error = Exception("Unknown Error")

        if config:
            self.config = config

    def post(self, url="", json_params="", **kwargs):
        return super().post(url, {"token": self.token}, json_params, **kwargs)

    @property
    def Index(self):
        return Index(self.project, self.task_type, self.tarsrc_name)

    def check_status(self, quiet=False):
        if self.status == -2:
            print(f"Task {self.task_id} is stopped.")
            return False
        if self.status == -1:
            print(f"Task {self.task_id} is paused.")
            return False
        if self.status == 0:
            if not quiet:
                print(f"Task {self.task_id} is waiting.")
        if self.status == 1:
            if not quiet:
                print(f"Task {self.task_id} is running.")
        if self.status == 2:
            return True

    def update_status(self):
        url_template = self.config.DragonURLTemplate
        try:
            api_address = self.config.ServerHost
        except AttributeError:
            error_print(
                "Library is not fully initialized: ServerHost is not set."
            )
            exit(1)
        port = self.config.ServerPort
        api_url = url_template.format(api_address, port)  # Dragon url
        res = requests.post(
            api_url % ("get_tasks_status"),
            data=json.dumps({"token": self.config.Token, "ids": [self.id]}),
            headers={
                "Content-Type": "application/json",
                "Connection": "close",
            },
        )
        self.status = json.loads(res.text)["result"][str(self.id)]

    @property
    def outpath(self):
        dirs = os.listdir(self.config.OutputDir)
        folder_name = next(
            filter(lambda _: _.split("_")[-1] == str(self.task_id), dirs)
        )
        return self.config.OutputDir / folder_name


def fillargs(f, args, kws):
    spec = inspect.getargspec(f)
    __args = spec.args[1:]
    print(spec.args)  # RM
    __defaults = spec.defaults
    result = dict().fromkeys(__args)
    # Default values
    __values = __args[::-1]
    __defaults = __defaults[::-1] if __defaults else []
    for i in range(len(__defaults)):
        result[__values[i]] = __defaults[i]

    for i in range(len(args)):
        result[__args[i]] = args[i]

    for k in result:
        if k in kws:
            result[k] = kws[k]

    return result, __args
