#!/usr/bin/env python

# https://packaging.python.org/en/latest/distributing.html
# https://tom-christie.github.io/articles/pypi/
# http://www.slideshare.net/jezdez/how-i-learned-to-stop-worrying-love-python-packaging
from setuptools import setup, find_packages
import sys, os

sys.path.append(os.getcwd())
from easypy import helpers


package = {
    "author" : "ludbek",
    "author_email" : "sth.srn@gmail.com",
    "long_description" : open("README.nf").read(),
    "url" : "https://github.com/ludbek/easypy",
    "license" : open("LICENSE.nf").read(),
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifier
    "classifiers" : "",
    "keywords" : "package manager, task executor, package creator",
    "packages" : find_packages(),
    "include_package_data" : True,
    "package_data" : {},
    "entry_points" : {
'console_scripts': [
            'py = easypy.core:router',
        ]
    },
}

c = helpers.Meta('meta.json')
package['name'] = c.get('name')
package['version'] = c.get('version')
package['description'] = c.get('description')
package['install_requires'] = c.get_requirements('prod')

setup(**package)

# configure virtualenvwrapper
path_to_bashrc = os.path.join(os.path.expanduser("~"), ".bashrc")
file = open(path_to_bashrc, 'r')
content = file.read()
file.close()

if not "source /usr/local/bin/virtualenvwrapper.sh" in content:
    vw_config = """
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
"""
    file = open(path_to_bashrc, 'a')
    file.write(vw_config)
    file.close()