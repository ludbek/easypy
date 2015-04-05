import re
import os
import json
import shutil
import sys
import ast
from string import Template


class Site:
    @classmethod
    def get_path(cls):
        return [p for p in sys.path if p.endswith('site-packages')][-1]

    @classmethod
    def detail_on(cls, package_name):
        """
        Return name and version of a package.
        """
        for pkg in cls.get_packages():
            if re.match(r"%s="%package_name, pkg):
                return pkg
        return False

    @classmethod
    def get_packages(cls):
        _, dirs, _ = next(os.walk(cls.get_path()))
        raw_packages = filter(lambda adir: 'info' in adir, dirs)
        packages = map(lambda pkg: re.sub(r"(?P<name>\w+)-(?P<version>[\d\.]+)\..*", "\g<name>==\g<version>", pkg), raw_packages)
        packages = map(lambda pkg: pkg.lower(), packages)
        return filter(lambda pkg: 'pip==' not in pkg and 'setuptools==' not in pkg, packages)

    @classmethod
    def has(cls, package_name):
        for pkg in cls.get_packages():
            if re.match(r"%s="%package_name, pkg) or package_name == pkg:
                return True
        return False


def get_afile(file_name):
    cwd = os.getcwd()
    while True:
        files = os.listdir(cwd)
        if file_name in files:
            return os.path.join(cwd, file_name)
        else:
            cwd = os.path.dirname(cwd)

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
    package_detail = "{package_name}=={version}".format(**package_data.groupdict())
    if package_detail[-1] is '.':
        package_detail = package_detail[:-1]
    return package_detail

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
        self.force
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

class Meta(object):
    """
    Gets and sets meta data.
    """
    def __init__(self, file_name):
        self.file_name = get_afile(file_name)
        self.file = open(self.file_name, 'r')
        self.data = json.loads(self.file.read())
        self.file.close()

    def get_requirements(self, env):
        requirements = self.data['requirements']['common']
        env_reqs = self.data['requirements'][env]
        if env_reqs:
            requirements.extend(env_reqs)
        return requirements

    def add_req(self, key, value):
        self.data['requirements'][key].append(value)
        self.save()

    def get(self, key):
        return self.data[key]

    def set(self, composite_key, value):
        if "requirements" in composite_key:
            print "let easypy handle the requirements :)"
        key = composite_key[0]
        self.data[key] = value
        self.save()

    def get_req(self, key):
        return self.data['requirements'][key]

    def remove_req(self, key, value):
        items = self.data['requirements'][key]
        to_remove = filter(lambda item: re.match(r'%s'%value, item), items)
        self.data['requirements'][key].remove(to_remove.pop())
        self.save()

    def update_req(self, key, hint, value):
        self.remove(key, hint)
        self.add(key, value)

    def save(self):
        self.file = open(self.file_name, 'w')
        data = json.dumps(self.data, indent = 4)
        self.file.write(data)
        self.file.close()
