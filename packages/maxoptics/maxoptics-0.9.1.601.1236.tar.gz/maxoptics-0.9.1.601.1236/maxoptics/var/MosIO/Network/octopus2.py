import asyncio
import json
import os
import time
from pprint import pprint as pp, pformat
from threading import Thread

import aiohttp
from socketIO_client import SocketIO, LoggingNamespace

from maxoptics.core.error import SimulationError
from maxoptics.core.logger import info_print, debug_print, error_print


def peek_task_status(project, task_info, client_ref, whale_client, config):
    task_id = task_info["id"]
    task_type = task_info["task_type"]

    project_id = project.id
    project_name = project.name

    def localtime():
        return time.asctime(time.localtime(time.time()))

    log_folder = project.log_folder
    destination = log_folder / f"{str(project_name)}_{str(task_id)}" / "log"
    os.makedirs(destination, exist_ok=True)
    with open(destination / "terminal.log", "w") as fs:
        fs.write("Waiting for response...")

    # Create socketIO client

    # sio_url = config.OctopusSIOTemplate.format(**config.__dict__)

    # ip, port = fstr(sio_url).removeprefix("http://").removeprefix("https://").split(":")
    ip, port = config.ServerHost, int(config.SocketPort)
    sio = SocketIO(ip, port, LoggingNamespace)
    info_print(
        f"From {config.ServerHost}:{config.SocketPort} retrieving task's printings..."
    )

    # Methods

    fs = open(destination / "terminal.log", "w")

    def pprint(msg):
        pp(msg, stream=fs) and fs.flush()

    # On Connect
    def connect():
        whale_client.start_time = localtime()
        whale_client.start_time_raw = time.time()
        pprint("Connected")
        debug_print("Socket Connected")
        fs.flush()

        # Immediately emit registration information
        debug_print("test_conn")
        sio.emit("test_conn")  # 测试连接
        sio.wait(seconds=1)

        debug_print("res_client")
        debug_print({"tid": task_id, "pid": project_id})
        sio.emit("res_client", '[{"id": %d}]' % task_id)  # TODO: Changed

    # On disconnect
    def disconnect():
        debug_print("Socket Disconnected")
        pprint("Disconnect")
        fs.flush()
        sio.disconnect()

    def terminal(res):
        debug_print("Socket Prints")
        fs.write("\n")
        pprint("Terminal")
        print(res)
        fs.flush()
        whale_client.status = 1

    def update(res):
        debug_print("Socket Updates")
        debug_print(res)
        print(res)
        # for k, v in json.loads(res).items():  # TODO: Changed
        #     # begin, end, progress, status, etc.
        #     setattr(whale_client, k, v)
        fs.flush()

    def error(res):
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

        sio.emit("disconnect")

        print(whale_client.error)
        exit(2)

    def test_conn(res):
        pprint("Test Connection")
        pprint(res)

    def register_all():
        sio.on("test_conn", test_conn)
        sio.on("update", update)
        sio.on("terminal", terminal)
        sio.on("error", error)
        sio.on("disconnect", disconnect)

        on_msg = "{}_DONE".format(task_type)

        def _done(res):
            debug_print("Task Succeed, Socket Terminates.")
            whale_client.end_time = localtime()
            whale_client.end_time_raw = time.time()

            # success_print(pformat(res))

            fs.write("\n")
            pprint(on_msg)
            pprint(res)

            whale_client.status = 2
            if not fs.closed:
                fs.close()

            sio.emit("disconnect")

        sio.on(on_msg, _done)

    register_all()

    def main():
        connect()
        debug_print("Start waiting")
        sio.wait()
        status = {-2: "Failed", -1: "Killed", 2: "Succeed"}[
            whale_client.status
        ]
        info_print(f"Task with {task_id} Stop Running with status {status}")

    c = client_ref()

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
                                print(status)
                                whale_client.status = status
                                whale_client.end_time = localtime()
                                whale_client.end_time_raw = time.time()
                                return
            await asyncio.sleep(5)
            if whale_client.status in [-2, -1, 2]:
                return

    w1 = Thread(target=main, daemon=True)
    # w2 = Thread(target=asyncio.run, args=(peek_dragon(),), daemon=True)
    w1.start()
    # w2.start()

    while int(whale_client.status) in [0, 1]:
        time.sleep(1)

    if sio.connected:
        # warnings.warn("Status from dragon, not Octopus(Refactored)")
        sio.disconnect()
