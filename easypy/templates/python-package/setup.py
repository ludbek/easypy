#!/usr/bin/env python

# https://packaging.python.org/en/latest/distributing.html
# https://tom-christie.github.io/articles/pypi/
# http://www.slideshare.net/jezdez/how-i-learned-to-stop-worrying-love-python-packaging
from setuptools import setup, find_packages
import sys, os

sys.path.append(os.getcwd())
from easypy import helpers


package = {
    "author" : "",
    "author_email" : "",
    "long_description" : open("README.nf").read(),
    "url" : "",
    "license" : open("LICENSE.nf").read(),
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifier
    "classifiers" : "",
    "keywords" : "",
    "packages" : find_packages(),
    "include_package_data" : True,
    "package_data" : {},
    "entry_points" : {
        'console_scripts': [
            '',
        ]
    },
}

c = helpers.Meta('meta.json')
package['name'] = c.get('name')
package['version'] = c.get('version')
package['description'] = c.get('description')
package['install_requires'] = c.get_requirements('prod')

setup(**package)