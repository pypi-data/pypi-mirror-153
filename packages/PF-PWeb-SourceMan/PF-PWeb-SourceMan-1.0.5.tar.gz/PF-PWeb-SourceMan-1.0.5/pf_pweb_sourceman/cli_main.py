import click
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.module.create_py_module import py_mod
from pf_pweb_sourceman.module.create_react_module import react_mod
from pf_pweb_sourceman.module.module_crud import crud
from pf_pweb_sourceman.prod.pweb_deployer import pweb_deployer
from pf_pweb_sourceman.pwebsm.descriptor_const import UIType, AppMode, CRUDAction, Boolean, DeployerAction, DeployerOS
from pf_pweb_sourceman.task.project_init import pi
from pf_pweb_sourceman.task.project_manager import pm


@click.group()
def bsw():
    console.blue("-------------------", bold=True)
    console.green("PWeb Source Manager", bold=True)
    console.blue("-------------------", bold=True)


@click.command(help="Setup PWeb Project from git repo")
@click.option("--repo", "-r", help="Give Project Git Repository", required=True)
@click.option("--directory", "-d", help="Project directory name", default=None, show_default=True)
@click.option("--branch", "-b", help="Enter project branch", default="dev", show_default=True)
@click.option("--environment", "-e", help="Enter project environment name", default=None, show_default=True)
@click.option("--mode", "-m", help="Enter Project Mode", default=AppMode.dev, show_default=True, type=click.Choice([AppMode.dev, AppMode.prod], case_sensitive=False))
def setup(repo, directory, branch, environment, mode):
    try:
        pm.setup(repo, directory, branch, mode, environment)
    except Exception as e:
        console.error(str(e))


@click.command(help="Download new changes and update the project")
@click.option("--mode", "-m", help="Enter Project Mode", default=AppMode.dev, show_default=True, type=click.Choice([AppMode.dev, AppMode.prod], case_sensitive=False))
@click.option("--environment", "-e", help="Enter project environment name", default=None, show_default=True)
def update(mode, environment):
    try:
        pm.update(mode, environment)
    except Exception as e:
        console.error(str(e))


@click.command(help="Initialize project from scratch")
@click.option("--name", "-n", help="Project name", default=None, show_default=True, required=True)
@click.option("--port", "-p", help="Project run on the port", default=1212, show_default=True, type=int)
@click.option("--directory", "-d", help="Project directory name", default=None, show_default=True)
@click.option("--mode", "-m", help="Enter Project Mode", default=AppMode.binary, show_default=True, type=click.Choice([AppMode.dev, AppMode.binary], case_sensitive=False))
@click.option("--ui-type", "-ui", help="Enter Project UI Type", default=UIType.ssr, show_default=True, type=click.Choice([UIType.react, UIType.ssr, UIType.api], case_sensitive=False))
def init(name, port, directory, mode, ui_type):
    try:
        pi.init(name, port, directory, mode, ui_type)
    except Exception as e:
        console.error(str(e))


@click.command(name="create-pymod", help="Create PWeb Module")
@click.option("--name", "-n", help="Module name", default=None, show_default=True, required=True)
@click.option("--url", "-u", help="Module repo url", default="#", show_default=True)
@click.option("--license", "-l", help="Module license", default="PF License", show_default=True)
@click.option("--author", "-a", help="Module author", default="PWeb", show_default=True)
@click.option("--authemail", "-ae", help="Module author email", default="problemfighter.com@gmail.com", show_default=True)
@click.option("--description", "-d", help="Module short description", default=None, show_default=True)
def create_module(name, url, license, author, authemail, description):
    try:
        py_mod.init(name, url, license, author, authemail, description)
    except Exception as e:
        console.error(str(e))


@click.command(name="create-react-mod", help="Create react module")
@click.option("--name", "-n", help="Enter UI module name", required=True, show_default=True)
@click.option("--modname", "-mn", help="Enter module name", required=True, show_default=True)
def create_react_module(name, modname):
    try:
        react_mod.init(name, modname)
    except Exception as e:
        console.error(str(e))


@click.command(help="Manipulate controller, create, delete etc.")
@click.option("--name", "-n", help="Enter controller name", required=True, show_default=True)
@click.option("--module", "-m", help="Enter module name", required=True, show_default=True)
@click.option("--action", "-a", help="Enter action", required=True, show_default=True, default=CRUDAction.create, type=click.Choice([CRUDAction.create, CRUDAction.delete]))
@click.option("--api", "-ap", help="Enter controller type", required=True, show_default=True, default=Boolean.yes, type=click.Choice([Boolean.yes, Boolean.no]))
def controller(name, module, action, api):
    try:
        crud.controller(name, module, action, api)
    except Exception as e:
        console.error(str(e))


@click.command(help="Manipulate DTO, create, delete etc.")
@click.option("--name", "-n", help="Enter DTO name", required=True, show_default=True)
@click.option("--module", "-m", help="Enter module name", required=True, show_default=True)
@click.option("--action", "-a", help="Enter action", required=True, show_default=True, default=CRUDAction.create, type=click.Choice([CRUDAction.create, CRUDAction.delete]))
def dto(name, module, action):
    try:
        crud.dto(name, module, action)
    except Exception as e:
        console.error(str(e))


@click.command(help="Manipulate model, create, delete etc. It can generate the whole set as well")
@click.option("--name", "-n", help="Enter model name", required=True, show_default=True)
@click.option("--module", "-m", help="Enter module name", required=True, show_default=True)
@click.option("--action", "-a", help="Enter action", required=True, show_default=True, default=CRUDAction.create, type=click.Choice([CRUDAction.create, CRUDAction.delete]))
@click.option("--all", "-al", help="Enter all (controller, dto, service)", required=True, show_default=True, default=Boolean.no, type=click.Choice([Boolean.yes, Boolean.no]) )
@click.option("--api", "-ap", help="Enter controller type", required=True, show_default=True, default=Boolean.yes, type=click.Choice([Boolean.yes, Boolean.no]))
def model(name, module, action, all, api):
    try:
        crud.model(name, module, action, all, api)
    except Exception as e:
        console.error(str(e))


@click.command(help="Manipulate service, create, delete etc.")
@click.option("--name", "-n", help="Enter service name", required=True, show_default=True)
@click.option("--module", "-m", help="Enter module name", required=True, show_default=True)
@click.option("--action", "-a", help="Enter action", required=True, show_default=True, default=CRUDAction.create, type=click.Choice([CRUDAction.create, CRUDAction.delete]))
def service(name, module, action):
    try:
        crud.service(name, module, action)
    except Exception as e:
        console.error(str(e))


@click.command(help="Deploy PWeb to server")
@click.option("--name", "-n", help="Enter app name", required=True, show_default=True)
@click.option("--domain", "-d", help="Enter domain or subdomain name", required=True, show_default=True)
@click.option("--os", "-os", help="Enter os name", required=True, show_default=True, default=DeployerOS.centos, type=click.Choice([DeployerOS.centos]))
@click.option("--action", "-a", help="Enter action", required=True, show_default=True, default=DeployerAction.deploy, type=click.Choice([DeployerAction.deploy]))
def deployer(name, domain, os, action):
    try:
        pweb_deployer.deploy(name, domain, os, action)
    except Exception as e:
        console.error(str(e))


bsw.add_command(setup)
bsw.add_command(update)
bsw.add_command(init)
bsw.add_command(create_module)
bsw.add_command(create_react_module)

bsw.add_command(controller)
bsw.add_command(model)
bsw.add_command(dto)
bsw.add_command(service)

bsw.add_command(deployer)
