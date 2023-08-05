import os
import sys
from pf_pweb_sourceman.pwebsm.pwebsm_resolver import PwebSMResolver
from pf_pweb_sourceman.task.git_repo_man import GitRepoMan
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pcli import pcli
from pf_pweb_sourceman.common.constant import CONST


class ProjectManager:
    git_repo_man = GitRepoMan()
    pwebsm_resolver = PwebSMResolver()

    def get_python(self):
        return sys.executable

    def setup(self, repo, directory, branch, mode, env):
        if not directory:
            directory = self.git_repo_man.get_repo_name_from_url(repo)
        project_root = self.pwebsm_resolver.project_root_dir(directory=directory)
        if PFPFFileUtil.is_exist(project_root):
            raise Exception("{} Path already exist.".format(str(project_root)))
        self._setup_or_update(root_path=project_root, repo=repo, branch=branch, mode=mode, env=env, directory=directory)

    def update(self, mode, env):
        root_path = os.getcwd()
        self._setup_or_update(root_path=root_path, repo=None, branch=None, mode=mode, env=env)

    def _setup_or_update(self, root_path, repo, branch, mode, env, directory=None):
        if repo and branch:
            self.git_repo_man.clone_or_pull_project(root_path, repo, branch)
        self.create_virtual_env(root_path)
        self.pwebsm_resolver.init_resolver(mode=mode, project_root=root_path, env=env, directory=directory)
        console.success("Process completed")

    def create_virtual_env(self, root):
        if not PFPFFileUtil.is_exist(os.path.join(root, CONST.VENV_DIR)):
            console.success("Creating virtual environment")
            pcli.run(self.get_python() + " -m venv " + CONST.VENV_DIR, root)


pm = ProjectManager()
