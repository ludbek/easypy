import os

from invoke import task, run
from invoke.exceptions import Failure

from easypy import helpers
from easypy.exceptions import TaskFailure

VIRTUALENV_HOME = os.getenv('WORKON_HOME')
PROJECT_HOME = os.getenv('PROJECT_HOME')

@task
def start(name, dir = None, python = None, force = False):
    """
    Creates a virtualenv for the new project. It works alongside with virtualenvwrapper.
    """
    project_env_path = "{}/{}".format(VIRTUALENV_HOME, name)
    if dir:
        project_path = '{}/{}'.format(helpers.get_abs_path(dir), name)
    else:
        project_home = os.getenv(PROJECT_HOME)
        if project_home:
            project_path = '{}/{}'.format(project_home, name)
        else:
            raise TaskFailure("Please pass project path or set 'PROJECT_HOME' environment variable.")
    # make project directory
    if force:
        # back up a directory if already exists
        if (os.path.exists(project_path)):
            run("mv {0} {0}-bck".format(project_path), pty = True)
    run("mkdir {}".format(project_path), pty = True)
    # create virtualenv
    run('virtualenv {}'.format(project_env_path))
    # create a link to project directory at project env directory
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
