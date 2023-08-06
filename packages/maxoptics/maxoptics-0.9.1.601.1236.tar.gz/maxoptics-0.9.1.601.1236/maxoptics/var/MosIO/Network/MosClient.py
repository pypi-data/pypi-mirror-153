import asyncio
import inspect
import json
import os
import re
import threading
import time
import warnings
from asyncio import events
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple

from maxoptics.config import BASEDIR, Config
from maxoptics.core import JSasync
from maxoptics.core.base import Material, Waveform
from maxoptics.core.base.BaseContainer import MaterialShell, WaveformShell
from maxoptics.core.base.task import TaskAbstract
from maxoptics.core.error import APIError, InvalidInputError, SimulationError
from maxoptics.core.logger import (
    debug_pprint,
    debug_print,
    error_print,
    info_print,
    success_print,
    warn_print,
)
from maxoptics.core.project.Project import ProjectCore
from maxoptics.core.project.ProjectBase import T
from maxoptics.core.utils.constraints import pr
from maxoptics.core.utils.currying import NONE, currying, fast_currying

from .BaseClient import BaseClient


class MaxOpticsBase(BaseClient):
    pass


class MaxOptics(BaseClient):
    def __init__(self):
        from maxoptics import __version__
        from maxoptics.var.MosIO import (
            PublicMaterials,
            UserMaterials,
            UserWaveforms,
        )

        if not Config.__from_MosLibrary__:
            warnings.warn(
                FutureWarning(
                    "You are initializing MaxOptics Instance directly by calling `MaxOptics().\n"
                    "Please use MosLibrary() instead.\n"
                    "P.S. Since version 0.9.1, the behaviour of MosLibrary() and MaxOptics() were diverged.\n"
                )
            )
            time.sleep(3)

        print(
            "====================================MaxOptics Studio==================================="
        )
        print(
            "=                                                                                     ="
        )
        print(
            "=                                 Copyright Infomation                                ="
        )
        print(
            "=           Built by Shanghai Maxoptics Information Technology Co.,Ltd.               ="
        )
        print(
            f"=                              Version: V{__version__} with GDS import                        ="
        )
        print(
            "=    Based on Python3.8+ and MOS suite Dragon, Octopus, Shark and Whale services      ="
        )
        print(
            "=                                                                                     ="
        )
        print(
            "======================================================================================="
        )

        super().__init__("DragonURLTemplate")
        self.projects: Dict[str, ProjectCore] = {}
        self.remote_projects = {}
        self.thread_status = True
        self.async_tasks = []

        self.public_materials = PublicMaterials(self)
        self.user_materials = UserMaterials(self, "passive")
        self.user_waveforms = UserWaveforms(self)

        # expired attrs
        self.materials = None
        self.waveforms = None

    def waiting(self):
        """Not in use."""
        t = threading.Thread(target=self.wait, name="Waiting")
        # t.setDaemon(True)
        t.start()

    def wait(self):
        """Not in use."""
        info_print("......", end=" ")
        while self.thread_status:
            info_print(".", end=" ", flush=True)
            time.sleep(1)

    def export_project(
        self, project: ProjectCore, name: str = None, _format="json"
    ) -> None:
        name = name if name else project.name
        proj_type = project.type
        params = {"token": self.token, "project_id": project.id}
        result = self.post(**params)
        if result["success"] is False:
            error_print("Export Failed, %s" % result["result"]["msg"])
            return
        else:
            os.makedirs(Config.OutputDir / "exports", exist_ok=True)

            fp = Config.OutputDir / "exports" / f"{name}.{proj_type}"
            info_print(f"Project {project.name} exported at {fp.absolute()}")
            with open(fp, "w") as f:
                if _format == "json":
                    f.write(json.dumps(result["result"], indent=4))
                else:
                    raise NotImplementedError("Not Implemented!")
            info_print("Project ", project.name, end=" ")
            success_print(" Exported.")
            return

    def delete_many_projects(self, projects_id):
        params = {"token": self.token, "projects_id": projects_id}
        result = self.post(**params)
        if result["success"] is False:
            error_print("Recover Project Failed, %s" % result["result"]["msg"])
            return
        else:
            return

    def import_project(
        self, name, path: str, verbose=False, **kwargs
    ) -> ProjectCore:
        project_type = str(path).split(".")[-1]
        with open(path) as f:
            data = json.load(f)
        public_material = self.search_public_materials()
        materials = data.get("materials", [])
        waveforms = data.get("waveforms", [])
        project = data["data"]
        exec_list = {"m": {}, "w": {}}

        for ret in public_material:
            exec_list["m"][str(ret["id"])] = ret["id"]

        material_creations = self.post(
            url="create_materials",
            token=self.token,
            materials_info=materials,
            project_type=project_type,
        )["result"]["result"]

        self.user_materials.reload()
        for i, ret in enumerate(material_creations):
            exec_list["m"][str(ret["original_id"])] = ret["id"]
            self.__fake_a_material(
                ret["id"],
                self.user_materials.ids,
                materials[i]["name"],
                self.user_materials.all(),
            )

        waveform_creations = self.post(
            url="create_waveforms", token=self.token, waveforms_info=waveforms
        )["result"]["result"]

        self.user_waveforms.reload()

        for i, ret in enumerate(waveform_creations):
            exec_list["w"][str(ret["original_id"])] = ret["id"]

            self.__fake_a_waveform(
                ret["id"],
                self.user_waveforms.ids,
                waveforms[i]["name"],
                self.user_waveforms.all(),
            )

        new_project = self.create_project_as(
            name=name, imported=True, project_type=project_type, **kwargs
        )
        new_project.appendix.update(dict(sweep=project["sweep"]))

        new_project.resize(
            project["tree"]["attrs"]["w"],
            project["tree"]["attrs"]["h"],
            project["tree"]["attrs"]["drawGrid"]["dx"],
            project["tree"]["attrs"]["drawGrid"]["dy"],
        )

        def rep(s: str):
            return re.sub(r"[()\-+]", "_", s)

        def ana(inp):
            if isinstance(inp, str):
                return f"'{inp}'"
            else:
                return inp

        def assign_value(lict, the_component):
            for attr in lict:
                if attr in ["name", "_objLink"]:
                    continue
                if the_component.get(attr, silent=True) is not None:
                    if isinstance(lict[attr], dict):
                        assign_value(lict[attr], the_component)
                    else:
                        if verbose:
                            print(
                                rep(the_component.name),
                                f'["{attr}"]',
                                "=",
                                str(ana(lict[attr])),
                                sep="",
                            )
                        the_component.set(
                            attr, deepcopy(lict[attr]), escape=["*"]
                        )

        assign_value(project["tree"]["attrs"], new_project.DOCUMENT)

        others = [project[_] for _ in project if _ != "tree"]

        children = project["tree"]["children"]

        import_component = self.import_component(
            assign_value, exec_list, new_project, project, rep, verbose
        )

        rec = 0
        while len(children) - rec:
            _rec = len(children)
            for ret in range(rec, len(children)):
                child = children[ret]
                children += child.get("children", [])
            rec = _rec

        for child in [
            _
            for _ in children
            if _["type"]["base"]["name"] == "ArithmeticObject"
        ]:
            debug_print("Import add " + child["name"] + child["type"]["name"])
            import_component(child)

        for other in others:
            if isinstance(other, list):
                for o in other:
                    import_component(o)
            else:
                import_component(other)

        for child in [
            _
            for _ in children
            if _["type"]["base"]["name"] != "ArithmeticObject"
        ]:
            import_component(child)

        new_project.save()
        return new_project

    @staticmethod
    @fast_currying
    def import_component(
        assign_value, exec_list, proj, project, rep, verbose, child
    ):
        if not isinstance(child, dict) or not child.get("type"):
            return
        component = proj.add(child["type"]["name"], child["name"])
        if verbose:
            print(
                rep(child["name"]),
                "=",
                proj.name,
                ".add(",
                '"{}", '.format(child["type"]["name"]),
                '"{}"'.format(child["name"]),
                ")",
                sep="",
            )
        assign_value(
            {"attrs": child["attrs"], "id": child.get("id")}, component
        )
        if component.get(
            "background_material", silent=True
        ) is not None and component.get("background_material"):
            component["background_material"] = exec_list["m"][
                str(component.get("background_material"))
            ]
        if component.get(
            "materialId", silent=True
        ) is not None and component.get("materialId"):
            component["materialId"] = exec_list["m"][
                str(component.get("materialId"))
            ]
        if component.get(
            "waveform_id", silent=True
        ) is not None and component.get("waveform_id"):
            component["waveform_id"] = exec_list["w"][
                str(component.get("waveform_id"))
            ]

    def create_project_as(
        self, name=None, imported=False, project_type="passive", **kwargs
    ):
        try:
            remote_projects = self.__search_projects_for_dolphin(
                pattern=name, batch_size=1000
            )
            if name:
                project_id = (
                    remote_projects[name]["id"]
                    if "id" in remote_projects[name]
                    else remote_projects[name]["project_id"]
                )
                project_version = (
                    remote_projects[name]["version"]
                    if "version" in remote_projects[name]
                    else remote_projects[name]["current_ptr"]
                )
            else:
                raise InvalidInputError(
                    "You may input one of: name, order, client.projects contains related information"
                )

        except KeyError:
            res = self.create_project(name, project_type, **kwargs)
            project_id = res.id
            project_version = res.version

        from maxoptics.var.project import MosProject

        project = self.projects[name] = MosProject(
            self, self.token, name, project_type=project_type, **kwargs
        )
        project.id = project_id
        project.version = project_version

        info_print("Project ", name, end=" ")
        success_print("Created.")
        info_print("project name: ", name)
        info_print("project id: ", self.projects[name].id)
        info_print("project version: ", self.projects[name].version)

        if not imported:
            info_print("This is a empty project, rebuilding needed")

        return project

    def ensure_materials(
        self, materials: List[Material], project_type: str, replace=False
    ):
        """Ensure the materials exist.
        If replace is set to True, this method will change existing materials' attribute.
        This action is kind of DANGEROUS because the same materials might be used in other projects,
        and you may change them unintentionally.

        Args:
            materials (list[Material]): A list of Material.

            project_type (str): Choose passive or active.

            replace (bool, optional): Whether to override the existing materials. Defaults to False.
        """
        from maxoptics.var.MosIO import UserMaterials

        assert isinstance(materials, list), "materials must be in list form!"

        used_names = UserMaterials(self, project_type).names
        used_ids = UserMaterials(self, project_type).ids
        new: List[Material] = []
        for i, info in enumerate(materials):
            assert isinstance(info, Material), "must be Material type!"
            if info.name in used_names:
                if replace:
                    new.append(info)
                for j, used_name in enumerate(used_names):
                    if used_name == info.name:
                        if replace:
                            self.delete_material(used_ids[j])
            else:
                new.append(info)

        res = self.__create_materials([_.to_dict() for _ in new], project_type)

        self.user_materials.reload()

        materials_id = self.user_materials.ids
        real_materials = self.user_materials.all()

        for i, m in enumerate(new):
            if (name := m.name) not in self.user_materials.names:
                evil_mat_id = res[i]["id"]
                self.__fake_a_material(
                    evil_mat_id, materials_id, name, real_materials
                )

    def __fake_a_material(
        self, evil_mat_id, materials_id, name, real_materials
    ):
        ind = materials_id.index(evil_mat_id)
        evil_material = real_materials[ind]
        fake_mat = MaterialShell({**evil_material.__raw__, "name": name})
        warn_print(
            f"Creation of {fake_mat} is rejected, replaced by {evil_material}"
        )
        self.user_materials._faked.append(fake_mat)

    def ensure_waveforms(self, waveforms: List[Waveform], replace=False):
        """Ensure the waveforms exist.
        If replace is set to True, this method will change existing waveforms' attribute.
        This action is kind of DANGEROUS because the same waveforms might be used in other projects,
        and you may change them unintentionally.

        Args:
            waveforms(list[Waveform]): A list of Waveform.

            replace(bool, optional): Whether to override the existing waveforms. Defaults to False.
        """
        from maxoptics.var.MosIO import UserWaveforms

        assert isinstance(waveforms, list), "waveforms must be in list form!"

        used_names = UserWaveforms(self).names
        used_ids = UserWaveforms(self).ids
        new = []
        for i, info in enumerate(waveforms):
            assert isinstance(info, Waveform), "must be Waveform type!"
            if info.name in used_names:
                if replace:
                    new.append(info)
                for j, used_name in enumerate(used_names):
                    if used_name == info.name:
                        if replace:
                            self.delete_waveform(used_ids[j])
            else:
                new.append(info)

        res = self.__create_waveforms([_.to_dict() for _ in new])

        self.user_waveforms.reload()

        waveforms_id = self.user_waveforms.ids
        real_waveforms = self.user_waveforms.all()

        for i, w in enumerate(new):
            if (name := w.name) not in self.user_waveforms.names:
                evil_waveform_id = res[i]["id"]
                self.__fake_a_waveform(
                    evil_waveform_id,
                    waveforms_id,
                    name,
                    real_waveforms,
                )

    def __fake_a_waveform(
        self, evil_waveform_id, waveforms_id, name, real_waveforms
    ):
        ind = waveforms_id.index(evil_waveform_id)
        evil_waveform = real_waveforms[ind]
        fake_waveform = WaveformShell({**evil_waveform.__raw__, "name": name})
        warn_print(
            f"Creation of {fake_waveform} is rejected, replaced by {evil_waveform}"
        )
        self.user_waveforms._faked.append(fake_waveform)

    def search_materials(self, url="") -> list:
        """
        搜索材料
        @param 空
        """
        params = {"token": self.token}

        result = self.post(url=url, **params)
        if result["success"] is False:
            error_print("Material search Failed, %s" % result["result"]["msg"])
            return []
        else:
            self.materials = result["result"]["result"]
            return result["result"]["result"]

    def search_public_materials(self) -> list:
        """
        搜索材料
        @param 空
        """
        params = {"token": self.token}

        result = self.post(url="get_public_materials", **params)
        if result["success"] is False:
            error_print("材料搜索失败, %s" % result["result"]["msg"])
            return []
        else:
            self.materials = result["result"]["public_materials"]
            return result["result"]["public_materials"]

    def search_waveforms(self) -> list:
        """ """
        params = {"token": self.token}

        result = self.post(**params)
        if result["success"] is False:
            error_print("Waveform search Failed, %s" % result["result"]["msg"])
            return []
        else:
            self.waveforms = result["result"]["result"]
            return result["result"]["result"]

    def create_project(self, name: str, project_type="passive", log_folder=""):
        """ """
        result = self.__initialize_project(name, project_type)

        from maxoptics.var.project import MosProject

        project = self.projects[name] = MosProject(
            self,
            self.token,
            name,
            project_type=project_type,
            log_folder=log_folder,
        )
        project.id = result["result"]["id"]
        project.type = project_type
        project.version = result["result"]["version"]

        # Print
        info_print("Project ", name, end=" ")
        success_print("Created.")
        info_print("project name: ", name)
        info_print("project id: ", self.projects[name].id)
        info_print("project version: ", self.projects[name].version)

        return project

    def __initialize_project(self, name, project_type):
        path = (
            Path(BASEDIR) / "var" / "models" / "const" / "ProjectSample.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            empty_project_data = json.load(f)

        params = {
            "token": self.token,
            "name": name,
            "data": empty_project_data,
            "dirty": True,
            "project_type": project_type,
        }
        result = self.post(url="create_project", **params)
        if result["success"] is False:
            error_print(
                "Project creation Failed, %s" % result["result"]["msg"]
            )
            raise ValueError(result["result"]["msg"])
        return result

    def save_project(self, project: ProjectCore, check=True):
        """ """

        project.DOCUMENT.attrs.exp_obj = {}
        params = project.format_components(
            container={
                "token": self.token,
                "id": project.id,
                "data": [],
            },
            key="data",
            check=check,
        )
        debug_pprint(json.loads(params))
        result = self.post(json_params=params)
        if result["success"] is False:
            error_print("Project save Failed, %s" % result["result"]["msg"])
        else:
            success_print("Project", project.name, "Saved.")

    def create_task(
        self,
        project: ProjectCore,
        task_type=None,
        **kws,
    ):
        pr().emit(project, "ProjectPreRun", task_type, [])
        _, get_callback = invoke_task(
            project=project,
            task_type=task_type,
            self=self,
            **kws,
        )
        return get_callback(self)

    def get_tasks(self, project, only_completed=False, **kws):
        """ """
        params = {
            "token": self.token,
            "project_id": project.id,
        }
        result = self.post(**params, **kws)
        if result["success"] is False:
            error_print("Search project Failed, %s" % result["result"]["msg"])
        else:
            silent = inspect.stack()[1][3] == "peek_task_status"
            if not silent:
                info_print("Project ", project.name, end=" ")
                success_print("Succeed.")
            project.tasks = result["result"]["tasklist"]
        return project.tasks

    def awaiting(self, depth=-1):
        dep = 0
        while self.async_tasks and (depth == -1 or dep < depth):
            this_round = [_.dest for _ in self.async_tasks]
            self.async_tasks = []
            comb = asyncio.gather(*this_round)
            loop = events.get_event_loop()
            loop.run_until_complete(comb)
            dep += 1

    def wait_latest(self):
        index = len(self.async_tasks) - 1
        temp_asys = [self.async_tasks.pop()]
        while temp_asys:
            this_round = [_.dest for _ in temp_asys]
            comb = asyncio.gather(*this_round)
            loop = events.get_event_loop()
            loop.run_until_complete(comb)
            temp_asys = (
                self.async_tasks[index:]
                if len(self.async_tasks) > index
                else []
            )

    def async_task(self, cor) -> JSasync:
        asynker = JSasync(cor, self.wait_latest)
        self.async_tasks.append(asynker)
        return asynker

    def async_create_task(
        self, proj, task_type=None, mode="", *args, **kwargs
    ) -> JSasync:
        task = self.create_task(
            proj, task_type, mode, 0, *args, __timeout__=-1, **kwargs
        )

        async def waiting():
            if not task:
                return
            while True:
                await asyncio.sleep(5)
                status = task.check_status(quiet=True)
                if status is not None:
                    if status:
                        return task
                    else:
                        return False

        return self.async_task(waiting())

    def delete_material(self, material_id):
        params = {"token": self.token, "material_id": material_id}
        result = self.post(url="delete_material", **params)
        if result["success"] is False:
            error_print("Delete Material Failed, %s" % result["result"]["msg"])
            raise APIError(
                "Delete Material Failed, %s" % result["result"]["msg"]
            )

    def delete_waveform(self, waveform_id):
        params = {"token": self.token, "waveform_id": waveform_id}
        result = self.post(url="delete_waveform", **params)
        if result["success"] is False:
            error_print("Delete Waveform Failed, %s" % result["result"]["msg"])
            raise APIError(
                "Delete Waveform Failed, %s" % result["result"]["msg"]
            )

    def __untrash_many_projects(self, id):
        params = {"token": self.token, "projects_id": [id]}
        result = self.post(url="untrash_many_projects", **params)
        if result["success"] is False:
            error_print("Recover Project Failed, %s" % result["result"]["msg"])
            return
        else:
            return

    def __search_projects_for_dolphin(
        self,
        group_id=0,
        trashed=False,
        page=0,
        pattern="",
        what_time="save_time",
        time_order=1,
        batch_size=1000,
    ) -> Dict[str, Any]:
        """Search projects.

        Returns:
            Dict[str, Any]: _description_
        """
        params = {
            "token": self.token,
            "group_id": group_id,
            "trashed": trashed,
            "page": page,
            "pattern": pattern,
            "what_time": what_time,
            "time_order": time_order,
            "batch_size": batch_size,
        }

        result = self.post(url="search_projects_for_dolphin", **params)
        remote_projects = {}

        if result["success"] is False:
            error_print("Search project Failed, %s" % result["result"]["msg"])

        else:
            projects = result["result"]["projects_info"]
            for project in projects:
                remote_projects[project["name"]] = project

        if not pattern:
            self.remote_projects = remote_projects

        return remote_projects

    def __create_materials(self, materials_info, project_type: str):
        params = {
            "token": self.token,
            "materials_info": materials_info,
            "project_type": project_type,
        }
        result = self.post(url="create_materials", **params)
        if result["success"] is False:
            error_print(
                "Material creation failed, %s" % result["result"]["msg"]
            )
        else:
            return result["result"]["result"]

    def __change_materials(self, materials_info):
        params = {"token": self.token, "materials_info": materials_info}
        result = self.post(url="change_materials", **params)
        if result["success"] is False:
            error_print(
                "Material modification failed, %s" % result["result"]["msg"]
            )
        else:
            return result["result"]

    def __create_waveforms(self, waveforms_info):
        """ """
        params = {"token": self.token, "waveforms_info": waveforms_info}
        result = self.post(url="create_waveforms", **params)
        if result["success"] is False:
            error_print(
                "Waveform creation Failed, %s" % result["result"]["msg"]
            )
        else:
            return result["result"]["result"]

    def __change_waveforms(self, waveforms_info):
        params = {"token": self.token, "waveforms_info": waveforms_info}
        result = self.post(url="change_waveforms", **params)
        if result["success"] is False:
            error_print(
                "Waveform modification failed, %s" % result["result"]["msg"]
            )
        else:
            return result["result"]

    search_projects = __search_projects_for_dolphin

    def get_material_table_data(self, material_id):
        params = {"token": self.token, "material_id": material_id}
        result = self.post(url="get_material_table_data", **params)
        if result["success"] is False:
            error_print(
                "Material table data fetching failed, %s"
                % result["result"]["msg"]
            )
        else:
            return result["result"]

    @staticmethod
    def get_uploader():
        from maxoptics.var.visualizer.main import UserImport

        return UserImport()

    def __del__(self):
        # self.logout()
        info_print("MaxOptics Studio SDK Exited")


@currying
def invoke_task(
    project: ProjectCore,
    task_type: str,
    __timeout__=-1,
    self: T = NONE,
    dep_task=0,
    task_info={},
    link_task_id=[],
    async_flag=True,
) -> Tuple[T, Any]:
    """Start a task.

    Args:
        project ():
        task_type ():
        __timeout__ ():
        self ():
        dep_task ():
        task_info ():
        link_task_id ():
        async_flag ():

    Returns:

    """
    from maxoptics.var.MosIO import get_callback
    from maxoptics.var.MosIO.Network.WhaleClient import WhaleClients

    assert isinstance(
        task_type, str
    ), "The param of create_task `task_type` must be string"

    debug_print(
        f"RUN TASK WITH {task_type = }, {async_flag = }, {dep_task = }"
    )

    if isinstance(dep_task, (TaskAbstract, WhaleClients)):
        dep_task = dep_task.id

    # project.save()
    if Config.Debug:
        project.export()

    params = dict(
        **{
            "token": self.token,
            "project_id": project.id,
            "tasktype": task_type,
            "dep_task": dep_task,
            "pid": project.id,
            "async": async_flag,
            "task_info": task_info,
            "link_task_id": link_task_id,
        }
    )

    # TODO: IO
    result = self.post(url="create_task", **params)

    if result["success"] is False:
        error_print("Task startup Failed, %s" % result["result"]["msg"])
        raise SimulationError(
            "Task startup Failed, %s" % result["result"]["msg"]
        )
    else:
        info_print("Project ", project.name)
        return self, get_callback(project, task_type, result)  # noqa
