import re
import os
import json
import shutil
import sys
from string import Template

from invoke import run

def get_abs_path(path):
    cwd = os.getcwd()
    if (re.match(r"./", path)):
        os.path.join(cwd, path)
    elif(re.match(r'^.$', path)):
        return cwd
    elif re.match(r"[^/]", path):
        os.path.join(cwd, path)
    else:
        return path

def get_site_dir():
    return [p for p in sys.path if p.endswith('site-packages')][-1]

def get_package_detail(package_name):
    """
    Return name and version of a package.
    """
    site_dir = get_site_dir()
    _, packages, _ = next(os.walk(site_dir))
    required_packages = filter(lambda item: re.match(r'%s'%package_name, item), packages)
    d_package = filter(lambda item: 'info' in item, required_packages).pop()
    package_data = re.search(r"(?P<package_name>.+?)-(?P<version>[\d\.]+)", d_package)
    return "{package_name}=={version}".format(**package_data.groupdict())

class CloneProject(object):
    def __init__(self, source_dir, dest_dir, kwargs, force = False):
        self.source = source_dir
        self.dest = dest_dir
        self.kwargs = kwargs
        self.force = force
        self.copy()
        self.render()

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

class Config(object):
    """
    Gets and sets configurations.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(self.file_name, 'r')
        self.data = json.loads(self.file.read())
        self.file.close()

    def add(self, key, value):
        self.file = open(self.file_name, 'w')
        self.data[key].append(value)
        self.save()

    def get(self, key):
        self.file = open(self.file_name, 'r')
        return self.data[key]

    def remove(self, key, value):
        self.file = open(self.file_name, 'w')
        items = self.data[key]
        to_remove = filter(lambda item: re.match(r'%s'%value, item), items)
        self.data[key].remove(to_remove.pop())
        self.save()

    def update(self, key, hint, value):
        self.file = open(self.file_name, 'w')
        self.remove(key, hint)
        self.add(key, value)

    def save(self):
        self.file.write(json.dumps(self.data, indent = 4))
        self.file.close()
