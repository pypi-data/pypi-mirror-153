import asyncio
import json
import os
import time
import weakref
from functools import partial
from pathlib import Path
from pprint import pprint as pp, pformat
from typing import Dict

import aiohttp
import requests
import socketio

from maxoptics.config import Config
from maxoptics.core.error import SimulationError
from maxoptics.core.logger import (
    error_print,
    info_print,
    logger,
    debug_print,
    success_print,
)
from maxoptics.core.utils.currying import currying

if Config.TestOctopusRefactor:
    from .octopus2 import peek_task_status
else:
    assert not hasattr(
        socketio, "__version__"
    ), "python-socketio version must be 5.0.0+"

    def peek_task_status(project, task_info, client_ref, whale_client, config):
        class Task:
            def __init__(self, **kwargs):
                for key, val in kwargs.items():
                    setattr(self, key, val)

        task = Task(**task_info)

        task_id = task_info["id"]
        task_type = task_info["task_type"]
        project_id = project.id

        c = client_ref()

        def localtime():
            return time.asctime(time.localtime(time.time()))

        log_folder = project.log_folder
        log_file_path = Config.TaskLogFileTemplate.format(
            project=project, task=task, log_folder=log_folder
        )

        success_print(
            "Task started. id: {}, task_type: {}.\n You can open file {} to check task status".format(
                str(task.id), str(task.task_type), log_file_path
            )
        )
        os.makedirs(Path(log_file_path).parent, exist_ok=True)
        with open(log_file_path, "w") as fs:
            fs.write("Waiting for response...")

        # Create socketIO client
        sio = socketio.AsyncClient(
            logger=logger,
            # reconnection_attempts=10,
            reconnection_attempts=0,
            reconnection_delay=5,
            reconnection_delay_max=10000000000,
            request_timeout=300,
        )
        fs = open(log_file_path, "w")

        def pprint(msg):
            pp(msg, stream=fs) and fs.flush()

        # On Connect
        @sio.event
        async def connect():
            whale_client.start_time = localtime()
            whale_client.start_time_raw = time.time()
            pprint("Connected")
            debug_print("Socket Connected")
            fs.flush()
            # Immediately emit registration information
            await sio.emit("res_client", [{"tid": task_id, "pid": project_id}])

            # subtasks = get_subtasks()
            # for subtask in subtasks:
            #     await sio.emit("res_client", [{"tid": subtask, "pid": project_id}])

        # On disconnect
        @sio.event
        async def disconnect():
            debug_print("Socket Disconnected")
            if not fs.closed:
                pprint("Disconnect")
                fs.flush()
            print()
            await sio.disconnect()

        @sio.event
        async def terminal(res):
            debug_print("Socket Prints")
            fs.write("\n")
            pprint("Terminal")
            pprint(res)
            fs.flush()
            whale_client.status = 1

        @sio.event
        async def update(res):
            debug_print("Socket Updates")
            if str(task_id) == str(res["task_id"]):
                for k, v in res.items():
                    # begin, end, progress, status, etc.
                    setattr(whale_client, k, v)
                fs.flush()
                progress = min(res["progress"], 100)

                miniprogress = round(progress / 2)
                info_print(
                    "%{prog} :[{wells}{points}]".format(
                        prog=progress,
                        wells="#" * miniprogress,
                        points="." * (50 - miniprogress),
                    ),
                    end="\r",
                )

                if whale_client.status == 2:
                    print()
                    await sio.disconnect()

        @sio.event
        async def error(res):
            debug_print("Socket Raises an Error")
            whale_client.end_time = localtime()
            whale_client.end_time_raw = time.time()

            error_print(pformat(res))

            fs.write("\n")
            pprint("ERROR")
            pprint(res)

            whale_client.status = -2
            whale_client.error = SimulationError(pformat(res))
            if not fs.closed:
                fs.close()

            await sio.emit("disconnect")
            await sio.disconnect()
            raise whale_client.error

        on_msg = "{}_DONE".format(task_type)

        @sio.on(on_msg)
        async def _done(res):
            debug_print("Task Succeed, Socket Terminates.")
            whale_client.end_time = localtime()
            whale_client.end_time_raw = time.time()

            # success_print(pformat(res))

            fs.write("\n")
            pprint(on_msg)
            pprint(f"Response from server is {res}.")

            whale_client.status = 2
            if not fs.closed:
                fs.close()

            print()
            await sio.emit("disconnect")
            await sio.disconnect()

        async def peek_dragon():
            while True:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        c.api_url % "get_tasks",
                        data=json.dumps(
                            {
                                "token": c.token,
                                "project_id": project_id,
                                "only_completed": False,
                            }
                        ),
                        headers={
                            "Content-Type": "application/json",
                            "Connection": "close",
                        },
                    ) as response:
                        response = await response.json()
                        if (result := response.get("result")) and (
                            tasks := result.get("tasklist")
                        ):
                            if matched_tasks := [
                                _ for _ in tasks if _["task_id"] == task_id
                            ]:
                                if (status := matched_tasks[0]["status"]) in [
                                    -2,
                                    -1,
                                    2,
                                ]:
                                    whale_client.status = status
                                    whale_client.end_time = localtime()
                                    whale_client.end_time_raw = time.time()
                                    return
                await asyncio.sleep(10)

        def get_subtasks():
            response = requests.post(
                c.api_url % "get_tasks",
                data=json.dumps(
                    {
                        "token": c.token,
                        "project_id": project_id,
                        "only_completed": False,
                        "all_pass": True,
                    }
                ),
                headers={
                    "Content-Type": "application/json",
                    "Connection": "close",
                },
            ).json()

            if (result := response.get("result")) and (
                tasks := result.get("tasklist")
            ):
                # "id", "name", "task_type", "status", "root_task"
                matched_tasks = [
                    _[0] for _ in tasks if _[4] == task_id and _[0] != task_id
                ]
                return matched_tasks
            else:
                return []

        async def main():
            if config.ListenSocket:
                sio_url = config.OctopusSIOTemplate.format(**config.__dict__)
                await sio.connect(sio_url, wait_timeout=30)

                info_print(f"From {sio_url} retrieving task's printings...\n")
                sio_wait = asyncio.create_task(sio.wait())
                waiting4 = [sio_wait]

            dragon_wait = asyncio.create_task(peek_dragon())
            waiting4 += [dragon_wait]

            done, pending = await asyncio.wait(
                waiting4, return_when="FIRST_COMPLETED"
            )
            status = {
                -2: "Failed",
                -1: "Killed",
                0: "Unfinished",
                1: "Unfinished",
                2: "Succeed",
            }[whale_client.status]
            info_print(
                f"Task with {task_id} Stop Running with status {status}"
            )

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None

        try:
            if loop and loop.is_running():
                print(
                    "Async event loop is running. Adding coroutine to the event loop."
                )
                tsk = loop.create_task(main())
                tsk.add_done_callback(
                    lambda t: print(
                        f"Task done with result={t.result()}  << return val of main()"
                    )
                )
            else:
                asyncio.run(main())
        except ValueError as e:
            error_print("Error happens: ", e)
            pass


@currying
def get_callback(project, task_type: str, result: Dict, self):
    task_info = dict(**result["result"], **{"task_type": task_type})
    ret = monitor_on(project, task_info, weakref.ref(self), self.config)
    project.running_tasks.append(ret)

    return ret


def monitor_on(project, task, client_ref, config):
    """Provide necessary parameters for ResultHandler

    Args:
        project (ProjectCore): The project object.
        task (dict[str, Any]): The task infos.
        client_ref (ReferenceType): weakref to client.
        config (ConfigFactory): config from client object, include token.

    Returns:
        Tuple: params for WhaleClient
    """
    result = task["id"], project, config
    functor = partial(
        peek_task_status,
        project=project,
        task_info=task,
        client_ref=client_ref,
        config=config,
    )
    return result, functor
