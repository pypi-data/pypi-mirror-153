import time

import zmq
from album.runner.album_logging import get_active_logger


class AlbumClient:

    def __init__(self, host, port):
        self.context = zmq.Context()
        self.port = port
        self.host = host
        self.rep = self.context.socket(zmq.REQ)
        self.url = "tcp://%s:%s" % (self.host, self.port)
        self.rep.connect(self.url)
        while True:
            get_active_logger().debug("Trying to connect to socket server...")
            self.rep.send_pyobj({"action": "ping"})
            message = self.rep.recv_pyobj()
            if message and "status" in message and message["status"] == 200:
                break
            time.sleep(0.2)

    def base(self):
        return self._handle_response(self._request_action('root'))

    def config(self):
        return self._handle_response(self._request_action('config'))

    def index(self):
        return self._handle_response(self._request_action('index'))

    def recently_launched(self):
        return self._handle_response(self._request_action('recently-launched'))

    def recently_installed(self):
        return self._handle_response(self._request_action('recently-installed'))

    def catalogs(self):
        return self._handle_response(self._request_action('catalogs'))

    def test(self, resolve_solution: str):
        return self._handle_response(self._request_solution_action('test', resolve_solution))

    def finish_tasks(self):
        return self._handle_response(self._request_action("finish_tasks"))

    def search(self, keywords):
        """Searches through album catalogs to find closest matching solution.
        """
        return self._handle_response(self._request_parameter_action('search', "keywords", keywords))

    def run(self, resolve_solution: str, args=None):
        return self._handle_response(self._request_solution_args_action('run', resolve_solution, args))

    def install(self, resolve_solution: str):
        return self._handle_response(self._request_solution_action('install', resolve_solution))

    def uninstall(self, resolve_solution: str):
        """Removes a solution from the disk. Thereby uninstalling its environment and deleting all its downloads.
        """
        return self._handle_response(self._request_solution_action('uninstall', resolve_solution))

    def get_task_status(self, task_id):
        return self._handle_response(self._request_parameter_action('status', "task_id", task_id))

    def deploy(self, deploy_path: str, catalog_name: str, dry_run: bool, push_option=None, git_email: str = None,
               git_name: str = None, force_deploy: bool = False, changelog: str = ""):
        """Function corresponding to the `deploy` subcommand of `album`.

        Generates the yml for a album and creates a merge request to the catalog only
        including the yaml and solution file.

        Args:
            force_deploy:
                Force overwrites a existing solution during deployment. Only for local catalogs.
            deploy_path:
                Path to a directory or a file.
                If directory: Must contain "solution.py" file.
            catalog_name:
                The catalog to deploy to. Either specify via argument in deploy-call, via url in solution or use
                default catalog.
            dry_run:
                When set, prepares deployment in local src of the catlog (creating zip, docker, yml),
                but not adding to the catalog src.
            push_option:
                Push options for the catalog repository.
            git_email:
                The git email to use. (Default: systems git configuration)
            git_name:
                The git user to use. (Default: systems git configuration)
            changelog:
                The change associated with this version of a solution compared to the last version.

        """
        raise NotImplementedError()

    def undeploy(self, solution_to_resolve: str, catalog_name: str, dry_run: bool, push_option=None, git_email: str = None,
                 git_name: str = None):
        """Function corresponding to the `undeploy` subcommand of `album`.

        Removes the solution from the given catalog.

        Args:
            solution_to_resolve:
                Solution identifier which should be removed (group:name:version).
            catalog_name:
                The catalog to remove the solution from.
            dry_run:
                When set, prepares undeploy in local src of the catalog,
                but not actually removing it the catalog src.
            push_option:
                Push options for the catalog repository.
            git_email:
                The git email to use. (Default: systems git configuration)
            git_name:
                The git user to use. (Default: systems git configuration)

        """
        raise NotImplementedError()

    def clone(self, path: str, target_dir: str, name: str) -> None:
        """
        Function corresponding to the `clone` subcommand of `album`.

        Args:
            path: the source of the clone command - a solution (group:name:version, path, or URL to file) or a catalog
                template string (i.e. template:catalog)
            target_dir: the directory where the cloned solution or catalog will be added to
            name: the name of the solution or catalog to be created

        """
        raise NotImplementedError()

    def shutdown(self):
        return self._handle_response(self._request_action('shutdown'))

    def upgrade(self, catalog_name=None, dry_run=False, override=False):
        return self._handle_response(self._request_action('upgrade'))

    def update(self, catalog_name=None):
        return self._handle_response(self._request_action('update'))

    def add_catalog(self, catalog_src):
        raise NotImplementedError()

    def remove_catalog_by_name(self, catalog_name):
        raise NotImplementedError()

    def is_installed(self, solution_to_resolve: str):
        res = self._handle_response(self._request_solution_action('status', solution_to_resolve))
        if res["status"] == 404:
            raise LookupError("Solution %s not found." % solution_to_resolve)
        return bool(res["installed"])

    def resolve(self, solution_to_resolve: str):
        res = self._handle_response(self._request_solution_action('resolve', solution_to_resolve))
        return res

    def dispose(self):
        get_active_logger().debug("Terminating Album socket client..")
        self.rep.disconnect(self.url)
        self.rep.close()
        self.context.term()
        get_active_logger().debug("Album socket client should be terminated.")

    def _request_action(self, action):
        self.rep.send_pyobj({"action": action})
        return self.rep.recv_pyobj()

    def _request_solution_action(self, action, resolve_solution):
        self.rep.send_pyobj({"action": action, "resolve_solution": resolve_solution})
        return self.rep.recv_pyobj()

    def _request_args_action(self, action, arg_name, arg_value):
        self.rep.send_pyobj({"action": action, arg_name: arg_value})
        return self.rep.recv_pyobj()

    def _request_solution_args_action(self, action, resolve_solution, args):
        self.rep.send_pyobj({"action": action, "resolve_solution": resolve_solution, "args": args})
        return self.rep.recv_pyobj()

    def _request_parameter_action(self, action, parameter_name, parameter):
        self.rep.send_pyobj({"action": action, parameter_name: parameter})
        return self.rep.recv_pyobj()

    def _handle_response(self, response):
        get_active_logger().debug("Album client received response: %s" % response)
        return response
