#!/usr/bin/env python

# Support setuptools only, distutils has a divergent and more annoying API and
# few folks will lack setuptools.
import os, sys
from setuptools import setup

sys.path.append(os.getcwd())
from __meta__ import meta
from easypy import helpers

c = helpers.Config('requirements.json')
meta['install_requires'] = c.get_requirements('prod')

setup(**meta)