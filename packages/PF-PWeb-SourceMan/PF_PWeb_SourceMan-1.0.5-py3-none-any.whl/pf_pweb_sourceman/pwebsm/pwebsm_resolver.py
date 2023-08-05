import glob
import os
import sys
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.constant import CONST
from pf_pweb_sourceman.pwebsm.descriptor_const import DesConst
from pf_pweb_sourceman.common.pcli import pcli
from pf_pweb_sourceman.task.git_repo_man import GitRepoMan
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_ymlenv.yml_util import YMLUtil


class PwebSMResolver:
    pwebsm_file_name = "pwebsm"
    pwebsm_file_extension = ".yml"
    git_repo_man = GitRepoMan()
    main_app_root = ""

    def project_root_dir(self, directory=None):
        root_path = os.getcwd()
        if directory:
            root_path = os.path.join(root_path, directory)
        return root_path

    def get_pwebsm_file_name(self, env=None):
        env_postfix = ""
        if env:
            env_postfix = "-" + env
        return self.pwebsm_file_name + env_postfix + self.pwebsm_file_extension

    def get_pwebsm_file(self, project_root=None, env=None, directory=None, pwebsm_yml_file=None):

        if not project_root:
            project_root = self.project_root_dir(directory)

        pwebsm_file = self.get_pwebsm_file_name(env)
        if not pwebsm_yml_file:
            pwebsm_yml_file = os.path.join(project_root, pwebsm_file)

        if not PFPFFileUtil.is_exist(pwebsm_yml_file):
            pwebsm_file = self.get_pwebsm_file_name()
            pwebsm_yml_file = os.path.join(project_root, pwebsm_file)

        if not PFPFFileUtil.is_exist(pwebsm_yml_file):
            console.error("{} file not found!".format(pwebsm_file))
            return None
        return pwebsm_yml_file

    def run_command_with_venv(self, root, command, mode):
        active = "source " + os.path.join(self.main_app_root, CONST.VENV_DIR, "bin", "activate")
        if sys.platform == "win32":
            active = os.path.join(self.main_app_root, CONST.VENV_DIR, "Scripts", "activate")
        command = active + " && " + command
        pcli.run(command, root, env=dict(os.environ, **{"source": mode}))

    def is_there_egg_info_file(self, path):
        files = glob.glob(os.path.join(path, "*.egg-info"))
        for file in files:
            console.yellow("Already Installed")
            return True
        return False

    def run_setup(self, root, run_type, mode):
        setup_file_name = "setup.py"
        setup_file = os.path.join(root, setup_file_name)
        if PFPFFileUtil.is_exist(setup_file) and not self.is_there_egg_info_file(root):
            command = "python " + setup_file_name + " " + run_type
            self.run_command_with_venv(root, command, mode)

    def run_py_command(self, root, command, mode):
        command = "python " + command
        self.run_command_with_venv(root, command, mode)

    def _get_value(self, dict_data, key, default=None):
        if key in dict_data:
            return dict_data[key]
        return default

    def _run_py_script(self, py_script, root_dir, mode):
        if not py_script or not root_dir or not PFPFFileUtil.is_exist(root_dir):
            return
        console.info("Resolving Dependencies")
        for directory in os.listdir(root_dir):
            project_root = os.path.join(root_dir, directory)
            for command in py_script:
                if command and command.startswith('setup.py'):
                    run_type = command.replace("setup.py", "").strip()
                    self.run_setup(project_root, run_type, mode=mode)
                else:
                    self.run_py_command(project_root, command=command, mode=mode)

    def _run_setup_py(self, lib_root, setup_py, mode):
        if setup_py:
            self.run_setup(lib_root, setup_py, mode)

    def _process_repo_clone(self, repo, branch, lib_root):
        branch = self._get_value(repo, DesConst.branch, branch)
        self.git_repo_man.clone_or_pull_project(path=lib_root, url=repo[DesConst.url], branch=branch)

    def _resolve_lib_dependency(self, project_root, mode, lib_root, env=None):
        pwebsm_yml_file = self.get_pwebsm_file(project_root=lib_root, env=env)
        if pwebsm_yml_file and PFPFFileUtil.is_exist(pwebsm_yml_file):
            self.process_pwebsm_file(project_root=project_root, mode=mode, pwebsm_yml_file=pwebsm_yml_file, env=env)

    def _process_dependency(self, mode, dependency, project_root, env=None):
        project_base_root = project_root
        if DesConst.dir in dependency:
            project_root = os.path.join(project_root, dependency[DesConst.dir])
        setup_py = self._get_value(dependency, DesConst.setup_py)

        yml_mode = self._get_value(dependency, DesConst.mode)
        if not yml_mode or mode not in yml_mode:
            console.error("There is no mode found")
            return

        branch = self._get_value(dependency, DesConst.branch)
        if not branch:
            console.error("Branch not found")
            return

        run_py_script = self._get_value(dependency, DesConst.run_py_script, [])
        self._run_py_script(run_py_script, root_dir=project_root, mode=mode)

        repos = self._get_value(dependency, DesConst.repo, [])
        for repo in repos:
            console.yellow("\nSTART ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
            try:
                if DesConst.url not in repo:
                    console.error("Invalid repo config")
                    continue

                repo_name = self.git_repo_man.get_repo_name_from_url(repo[DesConst.url])
                if DesConst.name in repo:
                    repo_name = repo[DesConst.name]

                lib_root = os.path.join(project_root, repo_name)
                self._process_repo_clone(repo, branch, lib_root)
                self._resolve_lib_dependency(project_root=project_base_root, lib_root=lib_root, mode=mode, env=env)
                self._run_setup_py(lib_root, setup_py, mode)
            except Exception as e:
                console.error(str(e))
            console.magenta("ENDED eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\n")

    def _run_before_start(self, yml, project_root, mode):
        if DesConst.before_start in yml:
            console.info("Running: Before start commands")
            for command in yml[DesConst.before_start]:
                console.success(command)
                self.run_command_with_venv(command=command, root=project_root, mode=mode)

    def _resolve_dependencies(self, yml_object, mode, project_root, key, env=None):
        if not yml_object:
            return

        dependencies = []
        if key in yml_object:
            dependencies = yml_object[key]

        for dependency in dependencies:
            self._process_dependency(mode, dependency, project_root, env)

    def _run_before_end(self, yml, root_path, mode):
        if DesConst.before_end in yml:
            console.info("Running: Before end commands")
            for command in yml[DesConst.before_end]:
                console.success(command)
                self.run_command_with_venv(command=command, root=root_path, mode=mode)

    def process_pwebsm_file(self, mode, project_root, env=None, directory=None, pwebsm_yml_file=None):
        pwebsm_yml_file = self.get_pwebsm_file(project_root, env=env, directory=directory, pwebsm_yml_file=pwebsm_yml_file)
        if not pwebsm_yml_file:
            return
        yml_object = YMLUtil.load_from_file(pwebsm_yml_file)
        self._run_before_start(yml_object, project_root, mode)
        self._resolve_dependencies(yml_object, mode, project_root, DesConst.dependencies)
        self._resolve_dependencies(yml_object, mode, project_root, DesConst.app_dependencies)
        self._run_before_end(yml_object, project_root, mode)

    def init_resolver(self, mode, project_root=None, env=None, directory=None):
        if not project_root:
            project_root = self.project_root_dir(directory)
        self.main_app_root = project_root
        self.process_pwebsm_file(mode=mode, project_root=project_root, env=env, directory=directory)
