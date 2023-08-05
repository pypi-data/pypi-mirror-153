import os.path
import re

from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pwebsm_util import PwebSMUtil
from pf_pweb_sourceman.pwebsm.descriptor_const import Boolean, CRUDAction
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_file.pfpf_text_file_man import TextFileMan
from pf_py_text.pfpt_string_util import PFPTStringUtil


class ModuleCRUD:

    def _validate_module(self, module_name):
        console.success("Validating module {}".format(module_name))
        app_root = PwebSMUtil.validate_app_root()
        module_root = os.path.join(app_root, module_name)
        module_package = os.path.join(module_root, PFPTStringUtil.find_and_replace_with(module_name, "-", "_"))
        if not PFPFFileUtil.is_exist(module_root):
            raise Exception("Invalid module, please check your module name or create one.")
        return module_package

    def validate_name(self, name):
        pattern = re.compile(r"([a-z]+[a-z0-9_]*)")
        response = pattern.fullmatch(name)
        if not response:
            raise Exception("Invalid name. Name can contain a-z, 0-9, _")

    def get_file_name(self, name):
        self.validate_name(name)
        return name.lower()

    def get_find_replace_dict(self, name):
        camel_name = PFPTStringUtil.underscore_to_camelcase(name)
        underscore_name = name.lower()
        url = PFPTStringUtil.find_and_replace_with(underscore_name, "_", "-")
        list_data = [
            {"find": "__LOWER__UNDERSCORE_NAME__", "replace": underscore_name},
            {"find": "__URL_NAME__", "replace": url},
            {"find": "__CAMEL_NAME__", "replace": camel_name},
        ]
        return list_data

    def create_file(self, name, dst_dir, src_file, dst_file):
        console.success("Creating {}".format(src_file))
        PFPFFileUtil.create_directories(dst_dir)
        dst = os.path.join(dst_dir, dst_file)
        if PFPFFileUtil.is_exist(dst):
            raise Exception("{} already exists!".format(dst_file))
        src = os.path.join(PwebSMUtil.get_template_pweb_mod_crud_dir(), src_file)

        init_file = "__init__.py"
        init_file_dst = os.path.join(dst_dir, init_file)
        if not PFPFFileUtil.is_exist(init_file_dst):
            PFPFFileUtil.copy(os.path.join(PwebSMUtil.get_template_pweb_mod_dir(), init_file), init_file_dst)

        PFPFFileUtil.copy(src, dst)
        fd_dict = self.get_find_replace_dict(name=name)
        TextFileMan.find_replace_text_content(dst, fd_dict)
        return dst

    def controller(self, name, module, action, is_api):
        module_root = self._validate_module(module)
        controller_dir = os.path.join(module_root, "controller")
        dst_file_name = self.get_file_name(name) + "_api_controller.py"
        template_name = "crud_api_controller.py"
        if is_api == Boolean.no:
            template_name = "crud_controller.py"
            dst_file_name = self.get_file_name(name) + "_controller.py"
        if action == CRUDAction.create:
            self.create_file(name, controller_dir, template_name, dst_file_name)
        console.yellow("Successfully Controller created!")

    def dto(self, name, module, action):
        module_root = self._validate_module(module)
        dto_dir = os.path.join(module_root, "dto")
        dst_file_name = self.get_file_name(name) + "_dto.py"
        template_name = "crud_dto.py"
        if action == CRUDAction.create:
            self.create_file(name, dto_dir, template_name, dst_file_name)
        console.yellow("Successfully DTO created!")

    def model(self, name, module, action, is_all, api):
        module_root = self._validate_module(module)
        model_dir = os.path.join(module_root, "model")
        dst_file_name = self.get_file_name(name) + ".py"

        template_name = "crud_model.py"
        if action == CRUDAction.create:
            self.create_file(name, model_dir, template_name, dst_file_name)
        console.yellow("Successfully Model created!")

        if is_all == Boolean.yes:
            self.controller(name, module, action, api)
            self.service(name, module, action)
            self.dto(name, module, action)

    def service(self, name, module, action):
        module_root = self._validate_module(module)
        service_dir = os.path.join(module_root, "service")
        dst_file_name = self.get_file_name(name) + "_service.py"

        template_name = "crud_service.py"
        if action == CRUDAction.create:
            self.create_file(name, service_dir, template_name, dst_file_name)
        console.yellow("Successfully Service created!")


crud = ModuleCRUD()
