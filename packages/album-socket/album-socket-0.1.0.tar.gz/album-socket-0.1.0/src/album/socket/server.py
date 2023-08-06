import json
import threading
import time
from json import JSONEncoder
from typing import Optional

import zmq
from album.api import Album
from album.core.api.controller.task_manager import ITaskManager
from album.core.model.default_values import DefaultValues
from album.core.utils.operations.solution_operations import serialize
from album.runner import album_logging
from album.runner.album_logging import get_active_logger

import album

module_logger = album_logging.get_active_logger


class AlbumSocketServer:
    port = DefaultValues.server_port.value

    def __init__(self, port: int):
        self.port = port
        self.album_instance: Optional[Album] = None
        self.context = None
        self.socket = None
        self.thread = None

    def setup(self, album_instance: Album):
        self.album_instance = album_instance

    def start(self):
        address = "tcp://*:%s" % self.port
        get_active_logger().debug("Launching zeromq TCP socket server at %s" % address)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(address)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.thread = threading.Thread(target=self._start, args=(get_active_logger().name, ))
        self.thread.start()

    def _start(self, parent_logger_name):
        album_logging.configure_logging("socket thread", parent_name=parent_logger_name)
        get_active_logger().debug('Starting thread listening to events...')
        self.running = True

        while True:
            #  Wait for next request from client
            message = self.socket.recv_pyobj()
            get_active_logger().debug("Received request: %s" % message)
            #  Send reply back to client
            if "action" in message and message["action"] == "TERMINATE":
                break
            result = self._process(message)
            self.socket.send_pyobj(result)
        get_active_logger().debug('Done with thread listening to events.')

    def shutdown(self):
        get_active_logger().debug("Album socket server: shutting down")
        shutdown_socket = self.context.socket(zmq.REQ)
        shutdown_socket.connect("tcp://127.0.0.1:%s" % self.port)
        shutdown_socket.send_pyobj({"action": "TERMINATE"})
        shutdown_socket.close()
        time.sleep(1)
        self.socket.close()
        if self.thread:
            self.thread.join()
        self.context.term()

    def _process(self, message):
        action = message["action"]
        if action == "index":
            return self._get_index()
        if action == "version":
            return self._get_version()
        if action == "config":
            return self._get_config()
        if action == "catalogs":
            return self._get_catalogs()
        if action == "recently_launched":
            return self._get_recently_launched_solutions()
        if action == "recently_installed":
            return self._get_recently_installed_solutions()
        if action == "run":
            resolve_solution = message["resolve_solution"]
            args = message["args"]
            return self._run(resolve_solution, args)
        if action == "install":
            resolve_solution = message["resolve_solution"]
            return self._install(resolve_solution)
        if action == "uninstall":
            resolve_solution = message["resolve_solution"]
            return self._uninstall(resolve_solution)
        if action == "test":
            resolve_solution = message["resolve_solution"]
            return self._test(resolve_solution)
        if action == "deploy":
            solution_path = message["solution_path"]
            catalog_name = message["catalog_name"]
            git_name = message["git_name"]
            git_email = message["git_email"]
            dry_run = message["dry_run"]
            return self._deploy(solution_path, catalog_name, git_name, git_email, dry_run)
        if action == "clone":
            if "resolve_solution" in message:
                resolve_solution = message["resolve_solution"]
                target_dir = message["target_dir"]
                name = message["name"]
                return self._clone_solution(resolve_solution, target_dir, name)
            else:
                template_name = message["template_name"]
                target_dir = message["target_dir"]
                name = message["name"]
                return self._clone_catalog(template_name, target_dir, name)
        if action == "status":
            if "resolve_solution" in message:
                resolve_solution = message["resolve_solution"]
                return self._status_solution(resolve_solution)
            else:
                task_id = message["task_id"]
                return self._status_task(task_id)
        if action == "resolve":
            resolve_solution = message["resolve_solution"]
            return self._resolve_solution(resolve_solution)
        if action == "add_catalog":
            src = message["src"]
            return self._add_catalog(src)
        if action == "remove_catalog":
            name = message["name"]
            return self._remove_catalog(name)
        if action == "upgrade":
            src = message["src"] if "src" in message else None
            name = message["name"] if "name" in message else None
            dry_run = message["dry_run"] if "dry_run" in message else False
            return self._upgrade(src, name, dry_run)
        if action == "update":
            src = message["src"] if "src" in message else None
            name = message["name"] if "name" in message else None
            return self._update(src, name)
        if action == "search":
            keywords = message["keywords"]
            return self._search(keywords)
        if action == "finish_tasks":
            return self._finish_tasks()
        if action == "ping":
            return {"status": 200}
        return {"status": 404, "message": "Not able to process action %s - action not found." % action}

    def _get_index(self):
        return self.album_instance.get_index_as_dict()

    @staticmethod
    def _get_version():
        return {
            "version": album.core.__version__,
            "author": album.core.__author__,
            "email": album.core.__email__
        }

    def _get_config(self):
        return {
            "cache_base": str(self.album_instance.configuration().base_cache_path())
        }

    def _get_catalogs(self):
        return self.album_instance.get_catalogs_as_dict()

    def _get_recently_launched_solutions(self):
        solutions = []
        for solution in self.album_instance.get_collection_index().get_recently_launched_solutions():
            solutions.append({
                'setup': solution.setup(),
                'internal': solution.internal()
            })
        return {'solutions': solutions}

    def _get_recently_installed_solutions(self):
        solutions = []
        for solution in self.album_instance.get_collection_index().get_recently_installed_solutions():
            solutions.append({
                'setup': solution.setup(),
                'internal': solution.internal()
            })
        return {'solutions': solutions}

    def _run(self, resolve_solution, args):
        args = self._get_arguments(args)
        task_id = self._run_solution_method_async(resolve_solution, self.album_instance.run, [args, False])
        return {"id": task_id, "msg": "process started"}

    def _install(self, resolve_solution):
        task_id = self._run_solution_method_async(resolve_solution, self.album_instance.install)
        return {"id": task_id, "msg": "process started"}

    def _uninstall(self, resolve_solution):
        task_id = self._run_solution_method_async(resolve_solution, self.album_instance.uninstall)
        return {"id": task_id, "msg": "process started"}

    def _test(self, resolve_solution):
        task_id = self._run_solution_method_async(resolve_solution, self.album_instance.test)
        return {"id": task_id, "msg": "process started"}

    def _deploy(self, solution_path, catalog_name, git_name, git_email, dry_run):
        push_options = None
        method = self.album_instance.deploy
        args = (solution_path, catalog_name, dry_run, push_options, git_name, git_email)
        task_id = self.album_instance.create_and_register_task(method, args)
        return {"id": task_id, "msg": "process started"}

    def _clone_solution(self, resolve_solution, target_dir, new_name):
        args = [target_dir, new_name]
        task_id = self._run_solution_method_async(resolve_solution, self.album_instance.clone, args)
        return {"id": task_id, "msg": "process started"}

    def _clone_catalog(self, template_name, target_dir, name):
        method = self.album_instance.clone
        args = tuple([template_name, target_dir, name])
        task_id = self.album_instance.create_and_register_task(method, args)
        return {"id": task_id, "msg": "process started"}

    def _status_solution(self, resolve_solution):
        try:
            solution = self.album_instance.resolve(resolve_solution)
            installed = self.album_instance.get_collection_index().is_installed(
                solution.catalog().catalog_id(),
                solution.coordinates()
            )
            return {
                "status": 200,
                "installed": installed
            }
        except LookupError:
            return {
                "status": 404,
                "description": "Solution not found"
            }

    class _JSONEncoder(JSONEncoder):
        def default(self, obj):
            serialize(obj)

    def _resolve_solution(self, resolve_solution):
        try:
            solution = self.album_instance.resolve(resolve_solution)
            return {
                "status": 200,
                "catalog_name": solution.catalog().name(),
                "setup": json.loads(self._JSONEncoder().encode(solution.database_entry().setup())),
                "internal": json.loads(self._JSONEncoder().encode(solution.database_entry().internal())),
            }
        except LookupError:
            return {
                "status": 404,
                "description": "Solution not found"
            }

    def _status_task(self, task_id):
        try:
            return self.album_instance.get_task_status(task_id)
        except LookupError:
            return {
                "status": 404,
                "description": f"Task not found with id {task_id}"
            }

    def _add_catalog(self, src):
        catalog = self.album_instance.add_catalog(src)
        catalog_id = catalog.catalog_id()
        return {"catalog_id": catalog_id}

    def _remove_catalog(self, name):
        self.album_instance.remove_catalog_by_name(name)

    def _upgrade(self, src, name, dry_run):
        if name is None and src is None:
            res = self.album_instance.upgrade(dry_run=dry_run)
        elif name is None:
            catalog = self.album_instance.get_catalog_by_src(src)
            res = self.album_instance.upgrade(catalog_name=catalog.name(), dry_run=dry_run)
        else:
            res = self.album_instance.upgrade(catalog_name=name, dry_run=dry_run)
        r = {}
        for catalog_name in res:
            r[catalog_name] = res[catalog_name].as_dict()
        return r

    def _update(self, src, name):
        if name is None and src is None:
            self.album_instance.update()
        elif name is None:
            catalog = self.album_instance.get_catalog_by_src(src)
            self.album_instance.update(catalog.name())
        else:
            self.album_instance.update(name)
        return {}

    def _search(self, keywords):
        return self.album_instance.search(keywords)

    def _finish_tasks(self):
        return self.album_instance.finish_tasks()

    def _run_solution_method_async(self, resolve_solution: str, method, args=None) -> str:
        task_args = [resolve_solution]
        if args:
            for arg in args:
                task_args.append(arg)
        task_id = self.album_instance.create_and_register_task(method, tuple(task_args))
        get_active_logger().debug("Album socket server: registered task %s" % task_id)
        return task_id

    @staticmethod
    def _get_arguments(args_json):
        command_args = [""]
        if args_json:
            for key in args_json:
                command_args.append(f"--{key}")
                command_args.append(str(args_json[key]))
        return command_args
