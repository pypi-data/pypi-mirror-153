import git
from git import Repo
from pf_pweb_sourceman.common.console import console
from pf_py_file.pfpf_file_util import PFPFFileUtil


class GitRepoMan:

    def get_repo_name_from_url(self, url: str):
        if not url:
            return None

        last_slash_index = url.rfind("/")
        last_suffix_index = url.rfind(".git")
        if last_suffix_index < 0:
            last_suffix_index = len(url)

        if last_slash_index < 0 or last_suffix_index <= last_slash_index:
            raise Exception("Invalid repo url {}".format(url))

        return url[last_slash_index + 1:last_suffix_index]

    def clone_or_pull_project(self, path, url, branch):
        repo_name = self.get_repo_name_from_url(url)
        if not repo_name:
            raise Exception("Invalid repo")
        if not PFPFFileUtil.is_exist(path):
            console.success("Cloning project: " + repo_name + ", Branch: " + branch)
            Repo.clone_from(url, branch=branch, to_path=path)
        else:
            console.success(repo_name + " Taking pull...")
            repo = Repo(path)

            repo.remotes.origin.fetch()
            local_branch_name = repo.active_branch.name

            console.info("Local branch name : " + local_branch_name + ", Checkout branch: " + str(branch))

            if local_branch_name != branch:
                repo.git.checkout(branch)
            # origin = repo.remotes.origin
            # origin.pull()
            git_repo = git.Git(path)
            response = git_repo.execute("git pull")
            print(response)
