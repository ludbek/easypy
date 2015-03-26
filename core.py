import sys
import os
from importlib import import_module

from invoke import cli
from invoke.exceptions import Failure
from invoke.tasks import Task
from invoke.collection import Collection

def get_site_dir():
    return [p for p in sys.path if p.endswith('site-packages')][-1]

def prepare_args(sys_args, package = None):
    site_dir = get_site_dir()
    tailored_args = []
    script = sys_args[0]
    if package:
        site_package = package
        task_n_args = sys_args[1:]
    else:
        site_package = sys_args[1]
        task_n_args = sys_args[2:]
    site_package_path = "%s/%s"%(site_dir, site_package)
    tailored_args.extend([script, '-r', site_package_path])
    tailored_args.extend(task_n_args)
    return tailored_args

def run_package_task(argv):
    """
    Run tasks in a site package.
    """
    _, site_packages, _ = next(os.walk(get_site_dir()))
    package_name = argv[1]
    if not package_name in site_packages:
        raise Exception
    cli.dispatch(prepare_args(argv))

def run_local_task(argv):
    """
    Run task in user's project directory.
    """
    task = argv[1]
    from invoke.loader import FilesystemLoader
    tasks = FilesystemLoader().load().task_names
    if not task in tasks.keys():
        raise Exception
    cli.dispatch(argv)

def run_ollo_task(argv):
    """
    Run task in ollo.
    """
    task = argv[1]
    from ollo import tasks
    tasks = Collection.from_module(tasks).task_names
    if not task in tasks.keys():
        raise Exception
    cli.dispatch(prepare_args(argv, 'ollo'))

def get_tasks(path = os.getcwd()):
    return None

def router(argv):
    # check the number of args
    ## if 3 args it could be for module
    ## if 2 args it could be for local or ollo tasks
    ### if 1 display help
    # assume the task is from module's directory
    try:
        run_package_task(argv)
    except Exception:
        pass
    # assume the task is from user's project directorys
    try:
        run_local_task(argv)
    except Exception:
        pass
    # assume the task is from ollo
    try:
        run_ollo_task(argv)
    except Exception:
        pass
