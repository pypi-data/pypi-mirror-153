import os.path
import re

from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pwebsm_util import PwebSMUtil
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_file.pfpf_text_file_man import TextFileMan
from pf_py_text.pfpt_string_util import PFPTStringUtil


class CreatePyModule:

    def validate_name(self, name):
        pattern = re.compile(r"([a-z]+[a-z0-9_\\-]*)")
        response = pattern.fullmatch(name)
        if not response:
            raise Exception("Invalid name. Name can contain a-z, 0-9, - , _")

    def check_module_availability(self, name):
        if not PFPFFileUtil.is_exist(PwebSMUtil.get_module_config_dir()):
            raise Exception("Please run the command inside project root")
        if PFPFFileUtil.is_exist(os.path.join(PwebSMUtil.get_module_app_dir(), name)):
            raise Exception("Sorry {} module already exist!".format(name))

    def create_structure(self, name, setup_info: list):
        template_root = PwebSMUtil.get_template_pweb_mod_dir()
        init_file = "__init__.py"
        readme_file = "README.md"
        setup_file = "setup.py"
        gitignore_file = ".gitignore"
        template_init_file = os.path.join(template_root, init_file)

        module_root = os.path.join(PwebSMUtil.get_module_app_dir(), name)
        PFPFFileUtil.create_directories(module_root)
        readme_source = os.path.join(template_root, readme_file)
        readme_dest = os.path.join(module_root, readme_file)

        setup_source = os.path.join(template_root, setup_file)
        setup_dest = os.path.join(module_root, setup_file)

        gitignore_source = os.path.join(template_root, gitignore_file)
        gitignore_dest = os.path.join(module_root, gitignore_file)

        PFPFFileUtil.copy(readme_source, readme_dest)
        PFPFFileUtil.copy(setup_source, setup_dest)
        PFPFFileUtil.copy(gitignore_source, gitignore_dest)

        TextFileMan.find_replace_text_content(setup_dest, setup_info)

        registry_name = PwebSMUtil.get_file_name(name)
        module_name = PFPTStringUtil.underscore_to_camelcase(registry_name)
        TextFileMan.find_replace_text_content(readme_dest, [
            {"find": "__MODULE_NAME__", "replace": PFPTStringUtil.human_readable(module_name)}
        ])

        module_pack_root = os.path.join(module_root, name)
        PFPFFileUtil.create_directories(module_pack_root)
        PFPFFileUtil.copy(template_init_file, os.path.join(module_pack_root, init_file))

        dirs = ["common", "controller", "data", "dto", "model", "service"]
        for dir_name in dirs:
            path = os.path.join(module_pack_root, dir_name)
            PFPFFileUtil.create_directories(path)
            PFPFFileUtil.copy(template_init_file, os.path.join(path, init_file))

        registry_source = os.path.join(template_root, "module_registry.py")

        registry_dest = os.path.join(module_pack_root, registry_name + "_registry.py")
        PFPFFileUtil.copy(registry_source, registry_dest)

        TextFileMan.find_replace_text_content(registry_dest, [
            {"find": "__MODULE_NAME__", "replace": module_name}
        ])

    def init(self, name, repo_url, license, author, author_email, description):
        console.success("Creating module {}".format(name))
        self.validate_name(name)
        self.check_module_availability(name)

        description_text = ""
        if description:
            description_text = description
        setup_info = [
            {"find": "__MODULE_NAME__", "replace": name},
            {"find": "__REPOSITORY_URL__", "replace": str(repo_url)},
            {"find": "__LICENSE_NAME__", "replace": str(license)},
            {"find": "__AUTHOR_NAME__", "replace": str(author)},
            {"find": "__AUTHOR_EMAIL__", "replace": str(author_email)},
            {"find": "__DESCRIPTION__", "replace": str(description_text)},
        ]
        self.create_structure(name, setup_info)
        console.success("Module has been created!")


py_mod = CreatePyModule()
