import re
import os
import shutil
from string import Template

from invoke import run

def get_abs_path(path):
    cwd = os.getcwd()
    if (re.match(r"./", path)):
        return '{}/{}'.format(cwd, path[2:])
    elif(re.match(r'^.$', path)):
        return cwd
    elif re.match(r"[^/]", path):
        return '{}/{}'.format(cwd, path)
    else:
        return path


class CloneProject(object):
    def __init__(self, source_dir, dest_dir, kwargs, force = False):
        self.source = source_dir
        self.dest = dest_dir
        self.kwargs = kwargs
        self.force = force

    def copy(self):
        """
        Creates a project directory from a template.
        """
        # copy project template
        force = self.force
        source_dir = self.source
        dest_dir = self.dest
        if self.force:
            if os.path.exists(dest_dir):
                bkup = '%s.bkup'%dest_dir
                if os.path.exists(bkup):
                    shutil.rmtree(bkup)
                shutil.copytree(dest_dir, bkup)
                shutil.rmtree(dest_dir)
        shutil.copytree(source_dir, dest_dir)

    def render(self, adir = None):
        """
        Recursively replace occurrence of keys with their respective values.
        """
        if not adir:
            adir = self.dest
        adir = os.path.abspath(adir)
        # prepare to render name
        old_name = adir
        new_name = old_name.format(**self.kwargs)
        if new_name is not old_name:
            os.rename(old_name, new_name)
        if os.path.isfile(new_name):
            # its a file
            self.render_file(new_name)
        else:
            # it is a directory
            stuff = os.listdir(new_name)
            for astuff in stuff:
                abs_path = '%s/%s'%(new_name, astuff)
                self.render(abs_path)

    def render_file(self, afile):
        """
        Replace occurrence of keys with their respective values for a file.
        """
        kwargs = self.kwargs
        f = open(afile, 'r')
        content = f.read()
        f.close
        f = open(afile, 'w')
        rendered_content = Template(content).safe_substitute(kwargs)
        f.write(rendered_content)
        f.close

