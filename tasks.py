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
