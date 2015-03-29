import os

from invoke import task, run
from invoke.exceptions import Failure

from easypy import helpers
from easypy.exceptions import TaskFailure

VIRTUALENV_HOME = os.getenv('WORKON_HOME')
PROJECT_HOME = os.getenv('PROJECT_HOME')

@task
def start(name, dir = None, version = None, package = False, force = False):
    """
    Creates a virtualenv for the new project. It works alongside with virtualenvwrapper.
    """
    project_env_path = os.path.join(VIRTUALENV_HOME, name)
    if dir:
        project_path = os.path.join(helpers.get_abs_path(dir), name)
    else:
        project_home = os.getenv(PROJECT_HOME)
        if project_home:
            project_path = os.path.join(project_home, name)
        else:
            raise TaskFailure("Please pass project path or set 'PROJECT_HOME' environment variable.")

    import easypy
    path_to_easypy = os.path.dirname(os.path.abspath(easypy.__file__))
    if package:
        template_name = "python-package"
    else:
        template_name = "regular"
    template_path = "%s/templates/%s"%(path_to_easypy, template_name)
    helpers.CloneProject(template_path, project_path, {'project_name' : name}, force)

    run('virtualenv {}'.format(project_env_path))
    run("echo {0} > {1}/.project".format(project_path, project_env_path))
    print "The project has been successfully created.\nTo work on it issue following command.\n$ workon %s"%name


@task
def end(name, all = False):
    """
    Remove a virtualenv related to project, {name}.
    If all is True, remove the project directory as well.
    """
    project_env_path = '{}/{}'.format(VIRTUALENV_HOME, name)
    if all:
        project_path_file = '{}/.project'.format(project_env_path)
        afile = open(project_path_file, 'r')
        project_path = afile.read()
        afile.close()
        print "Removing {}".format(project_path)
        run('rm -RI {}'.format(project_path), pty = True)
    print "Removing {}".format(project_env_path)
    run('rm -RI {}'.format(project_env_path), pty = True)


@task
def add(package, dev = False, test = False, prod = False):
    """
    Add a package.
    """
    run("pip install %s"%package, pty = True)
    c = helpers.Config('requirements.json')
    package_detail = helpers.get_package_detail(package)
    if dev:
        c.add('dev', package_detail)
    elif test:
        c.add('test', package_detail)
    elif prod:
        c.add('prod', package_detail)
    else:
        c.add('common', package_detail)

@task
def remove(package, dev = False, test = False, prod = False):
    """
    Remove a package.
    """
    run("pip uninstall %s"%package, pty = True)
    c = helpers.Config('requirements.json')
    if dev:
        c.remove('dev', package)
    elif test:
        c.remove('test', package)
    elif prod:
        c.remove('prod', package)
    else:
        c.remove('common', package)


@task
def update(package):
    """
    Update a package.
    """
    remove(package)
    add(package)

@task
def list(name, dev = False, test = False, prod = False, all = False):
    """
    List installed packages.
    """
    # list packages at respective sector
    pass

@task
def search(name):
    """
    Search for a package.
    """
    pass

@task
def about(name, package):
    """
    Give information on a project.
    """
    pass