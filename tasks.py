from invoke import task, run
from invoke.exceptions import Failure
import os

@task
def hero():
    run("echo 'xoxo'", pty=True)
