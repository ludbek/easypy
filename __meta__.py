from setuptools import setup, find_packages
# https://packaging.python.org/en/latest/distributing.html
# https://tom-christie.github.io/articles/pypi/
# http://www.slideshare.net/jezdez/how-i-learned-to-stop-worrying-love-python-packaging
meta = {
    "name" : "easypy",
    "version" : "0.0.0",
    "description" : "A package manager, package creator and task executor for python.",
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
