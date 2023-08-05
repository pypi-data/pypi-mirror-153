import os
import re

from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pwebsm_util import PwebSMUtil
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_file.pfpf_text_file_man import TextFileMan
from pf_py_text.pfpt_string_util import PFPTStringUtil


class CreateReactModule:

    def validate_name(self, name):
        pattern = re.compile(r"([a-z]+[a-z0-9\\-]*)")
        response = pattern.fullmatch(name)
        if not response:
            raise Exception("Invalid name. Name can contain a-z, 0-9, - ")

    def get_module_ui_path(self, module_name):
        return os.path.join(PwebSMUtil.get_module_app_dir(), module_name, "ui")

    def check_module_availability(self, module_name):
        if not PFPFFileUtil.is_exist(PwebSMUtil.get_module_config_dir()):
            raise Exception("Please run the command inside project root")

        if not PFPFFileUtil.is_exist(os.path.join(PwebSMUtil.get_module_app_dir(), module_name)):
            raise Exception("Create the module named {} first.".format(module_name))

        if PFPFFileUtil.is_exist(self.get_module_ui_path(module_name)):
            raise Exception("Sorry {} module UI already exist!".format(module_name))

    def create_structure(self, name, module_name):
        ui_root = self.get_module_ui_path(module_name)
        PFPFFileUtil.create_directories(ui_root)

        dirs = ["app", "tdef", "package.json", "tsconfig.json"]
        for dir_name in dirs:
            source = os.path.join(PwebSMUtil.get_template_react_mod_dir(), dir_name)
            destination = os.path.join(ui_root, dir_name)
            PFPFFileUtil.copy(source, destination)

        package_json = os.path.join(ui_root, "package.json")
        module_config = os.path.join(ui_root, "app", "view", "module-config.ts")
        module_config_rename = os.path.join(ui_root, "app", "view", name + "-config.ts")
        klass_name = PFPTStringUtil.underscore_to_camelcase(name, "-")

        TextFileMan.find_replace_text_content(package_json, [
            {"find": "__MODULE_NAME__", "replace": name}
        ])

        TextFileMan.find_replace_text_content(module_config, [
            {"find": "__MODULE_NAME__", "replace": klass_name}
        ])

        PFPFFileUtil.rename(module_config, module_config_rename)

    def init(self, name, module_name):
        console.success("Creating module {} UI".format(module_name))
        self.validate_name(name)
        self.check_module_availability(module_name)
        self.create_structure(name, module_name)
        console.success("UI Module has been created!")


react_mod = CreateReactModule()
