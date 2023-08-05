import os

from pf_pweb_sourceman.pwebsm.descriptor_const import DesConst
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_text.pfpt_string_util import PFPTStringUtil


class PwebSMUtil:

    @staticmethod
    def get_root_dir():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def get_template_dir():
        return os.path.join(PwebSMUtil.get_root_dir(), "template")

    @staticmethod
    def get_template_common_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "common")

    @staticmethod
    def get_template_prod_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "prod")

    @staticmethod
    def get_template_prod_centos_dir():
        return os.path.join(PwebSMUtil.get_template_prod_dir(), "centos")

    @staticmethod
    def get_template_pweb_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "pweb")

    @staticmethod
    def get_template_pweb_mod_dir():
        return os.path.join(PwebSMUtil.get_template_pweb_dir(), "module")

    @staticmethod
    def get_template_pweb_mod_crud_dir():
        return os.path.join(PwebSMUtil.get_template_pweb_mod_dir(), "crud")

    @staticmethod
    def get_template_react_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "react")

    @staticmethod
    def get_template_react_mod_dir():
        return os.path.join(PwebSMUtil.get_template_react_dir(), "module")

    @staticmethod
    def get_module_dir():
        return os.getcwd()

    @staticmethod
    def get_module_app_dir():
        return os.path.join(PwebSMUtil.get_module_dir(), DesConst.app_dependencies_dir)

    @staticmethod
    def get_module_config_dir():
        return os.path.join(PwebSMUtil.get_module_app_dir(), "config")

    @staticmethod
    def get_file_name(name):
        text = PFPTStringUtil.find_and_replace_with(name, "-", "_")
        text = PFPTStringUtil.replace_space_with(text)
        return text.lower()

    @staticmethod
    def validate_app_root():
        if not PFPFFileUtil.is_exist(PwebSMUtil.get_module_app_dir()):
            raise Exception("Please run the command inside project root")
        return PwebSMUtil.get_module_app_dir()
