import sys
import os
from importlib import import_module

from invoke import cli
from invoke.exceptions import Failure
from invoke.tasks import Task
from invoke.collection import Collection

from easypy.exceptions import TaskNotAvailable, PackageNotAvailable

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
        raise PackageNotAvailable(package_name)
    # if length of argv is 2, the request is in format $ py <package>
    # list the tasks in package
    if len(argv) == 2:
        argv.append('-l')
    cli.dispatch(prepare_args(argv))

def run_local_task(argv):
    """
    Run task in user's project directory.
    """
    task = argv[1]
    from invoke.loader import FilesystemLoader
    tasks = FilesystemLoader().load().task_names
    if task == 'tasks':
        argv[1] = '-l'
        cli.dispatch(argv)
        return True
    if not task in tasks.keys():
        raise TaskNotAvailable(task)
    cli.dispatch(argv)

def run_ollo_task(argv):
    """
    Run task in ollo.
    """
    from ollo import tasks
    tasks = Collection.from_module(tasks).task_names
    if len(argv) == 1:
        # the request is in the format $ py
        # display each tasks and ways to get help on them
        print "Available tasks:\n"
        for task in tasks:
            print "\t%s\n"%task

    else:
        # the request is in the format $ py <task>
        task = argv[1]
        if not task in tasks.keys():
            raise TaskNotAvailable(task)
        cli.dispatch(prepare_args(argv, 'ollo'))

def get_tasks(path = os.getcwd()):
    return None

def router(argv):
    """
    Dispatch appropriate task.
    """
    # assume the task is from module's directory
    try:
        run_package_task(argv)
    except PackageNotAvailable as e:
        pass
    # assume the task is from user's project directorys
    try:
        run_local_task(argv)
    except TaskNotAvailable as e:
        pass
    # assume the task is from ollo
    try:
        run_ollo_task(argv)
    except TaskNotAvailable as e:
        print e
