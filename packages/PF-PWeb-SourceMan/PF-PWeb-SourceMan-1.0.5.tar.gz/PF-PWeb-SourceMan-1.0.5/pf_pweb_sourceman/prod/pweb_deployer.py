import os

from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pwebsm_util import PwebSMUtil
from pf_pweb_sourceman.pwebsm.descriptor_const import DeployerAction, DeployerOS
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_file.pfpf_text_file_man import TextFileMan


class PWebDeployer:

    def check_basic_validity(self):
        if not PFPFFileUtil.is_exist(PwebSMUtil.get_module_config_dir()):
            raise Exception("Please run the command inside project root")

    def create_file(self, src_file, dst_file, find_replace: list):
        PFPFFileUtil.copy(src_file, dst_file)
        TextFileMan.find_replace_text_content(dst_file, find_replace)
        return dst_file

    def create_centos_prod(self, name, application_root, domain):
        console.success("Creating Production Files")
        unix_socket_path = "unix:" + os.path.join(application_root, "PWeb.sock")
        fd_dict = [
            {"find": "___DOMAIN_NAME___", "replace": domain},
            {"find": "___UNIX_SOCK___", "replace": unix_socket_path},
            {"find": "___APP_NAME___", "replace": name},
            {"find": "___PROJECT_ROOT___", "replace": application_root},
        ]
        dsc_root = os.path.join(application_root, "prod")
        PFPFFileUtil.create_directories(dsc_root)
        service_src = os.path.join(PwebSMUtil.get_template_prod_centos_dir(), "application.service")
        service_dst = os.path.join(dsc_root, domain + ".service")

        nginx_src = os.path.join(PwebSMUtil.get_template_prod_centos_dir(), "nginx.conf")
        nginx_dst = os.path.join(dsc_root, domain + ".conf")

        self.create_file(service_src, service_dst, fd_dict)
        self.create_file(nginx_src, nginx_dst, fd_dict)
        console.success("Created Production Files")

    def deploy_on_os(self, name, domain, _os):
        application_root = PwebSMUtil.get_module_dir()
        if _os == DeployerOS.centos:
            self.create_centos_prod(name, application_root, domain)
        else:
            console.error("Invalid OS Selected")

    def deploy(self, name, domain, _os, action):
        self.check_basic_validity()
        if action == DeployerAction.deploy:
            self.deploy_on_os(name, domain, _os)
        else:
            console.error("Invalid Action")


pweb_deployer = PWebDeployer()
