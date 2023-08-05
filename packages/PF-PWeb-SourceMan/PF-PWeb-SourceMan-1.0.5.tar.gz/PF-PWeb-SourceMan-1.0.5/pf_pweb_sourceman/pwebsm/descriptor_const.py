class DeployerAction:
    deploy = "deploy"


class DeployerOS:
    centos = "centos"


class CRUDAction:
    create = "create"
    delete = "delete"


class Boolean:
    yes = "yes"
    no = "no"


class UIType:
    react = "react"
    ssr = "ssr"
    api = "api"


class AppMode:
    dev = "dev"
    prod = "prod"
    all = "all"
    binary = "binary"


dev_dependency_dir = "dev-dependencies"


class DesConst:
    before_start = "before_start"
    app_dependencies = "app_dependencies"
    pip_install = "pip_install"
    dependencies = "dependencies"
    before_end = "before_end"

    # INTERNAL
    dir = "dir"
    setup_py = "setup-py"
    branch = "branch"
    run_py_script = "run-py-script"
    mode = "mode"
    repo = "repo"
    name = "name"
    url = "url"

    # Some Values
    app_dependencies_dir = "application"
    dev_dependencies_dir = dev_dependency_dir
    ui_dependencies_dir = dev_dependency_dir + "/ui"
