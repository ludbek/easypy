import sys
import os
from importlib import import_module
import re

from invoke import cli
from invoke.exceptions import Failure, CollectionNotFound
from invoke.tasks import Task
from invoke.collection import Collection

from easypy.exceptions import TaskNotAvailable, PackageNotAvailable, InvalidPackage

def get_site_dir():
    return [p for p in sys.path if p.endswith('site-packages')][-1]

def prepare_args(sys_args, package = None):
    tailored_args = []
    script = sys_args[0]
    if package:
        site_dir = get_site_dir()
        site_package = package
        task_n_args = sys_args[1:]
        site_package_path = "%s/%s"%(site_dir, site_package)
    else:
        # it is for easypy
        # start and end command is executed when easypy is not installed in virtualenv
        # so this exception is necessary
        import easypy
        site_package_path = easypy.__path__[0]
        task_n_args = sys_args[1:]
    tailored_args.extend([script, '-r', site_package_path])
    tailored_args.extend(task_n_args)
    return tailored_args

def print_title(title):
    print title
    print '-'*20

def is_valid_package(package_name):
    """
    Checks if a package at site directory has tasks.
    """
    try:
        apackage = import_module('%s.tasks'%package_name)
    except ImportError:
        return False
    tasks = Collection.from_module(apackage).task_names
    if tasks == {}:
        return False
    return True

def display_tasks_everywhere():
    """
    Display tasks in easypy, project directory and packages in site directory.
    TODO: bug here, every call to dispatch ends the entire process tree.
    """
    display_easypy_tasks()
    display_local_tasks()
    # walk through every packages in site_packages directory
    _, packages, _ = next(os.walk(get_site_dir()))
    valid_packages = filter(lambda package: not re.search(r'info$', package), packages)
    for package in valid_packages:
        display_apackage_tasks(package)

def display_easypy_tasks():
    print_title("At easypy")
    argv = ['xxx.py']
    argv.append('-l')
    cli.dispatch(prepare_args(argv))

def display_local_tasks():
    print_title("In this project")
    cli.dispatch(['xxx.py', '-l'])

def display_apackage_tasks(package_name):
    """
    Display tasks in a site package.
    """
    argv = ['xxx']
    argv.append('-l')
    print_title("In %s"%package_name)
    cli.dispatch(prepare_args(argv, package_name))

def run_package_task(argv):
    """
    Run tasks in a site package.
    """
    _, site_packages, _ = next(os.walk(get_site_dir()))
    package_name = argv[1]
    if not package_name in site_packages:
        raise PackageNotAvailable(package_name)
    if not is_valid_package(package_name):
        raise InvalidPackage(package_name)
    # if length of argv is 2, the request is in format $ py <package>
    # list the tasks in package
    if len(argv) == 2:
        display_apackage_tasks(package_name)
        return
    cli.dispatch(prepare_args(argv))

def run_local_task(argv):
    """
    Run task in user's project directory.
    """
    task = argv[1]
    from invoke.loader import FilesystemLoader
    try:
        tasks = FilesystemLoader().load().task_names
    except CollectionNotFound:
        raise TaskNotAvailable(task)
    if task == '.':
        display_local_tasks()
        return
    if not task in tasks.keys():
        raise TaskNotAvailable(task)
    cli.dispatch(argv)

def run_easypy_task(argv):
    """
    Run task in easypy.
    """
    from easypy import tasks
    tasks = Collection.from_module(tasks).task_names
    if len(argv) == 1:
        # the request is in the format $ py
        # display available tasks in easypy
        display_easypy_tasks()
    else:
        # the request is in the format $ py <task>
        task = argv[1]
        if not task in tasks.keys():
            raise TaskNotAvailable(task)
        cli.dispatch(prepare_args(argv))

def router(argv = None):
    """
    Dispatch to appropriate task.
    """
    if not argv:
        argv = sys.argv
    if len(argv) == 1:
        run_easypy_task(argv)
        return
    if argv[1] in ['start', 'end', 'setup', 'register', 'deploy']:
        run_easypy_task(argv)
        return
    if len(argv) == 2 and argv[1] in ['-a', '--all']:
        display_tasks_everywhere()
        return
    # assume the task is from module's directory
    try:
        run_package_task(argv)
    except (PackageNotAvailable, InvalidPackage):
        pass
    # assume the task is from user's project directorys
    try:
        run_local_task(argv)
    except TaskNotAvailable:
        pass
    # assume the task is from easypy
    try:
        run_easypy_task(argv)
    except TaskNotAvailable as e:
        print e
