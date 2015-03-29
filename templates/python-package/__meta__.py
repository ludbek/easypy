# https://packaging.python.org/en/latest/distributing.html
# https://tom-christie.github.io/articles/pypi/
# http://www.slideshare.net/jezdez/how-i-learned-to-stop-worrying-love-python-packaging
meta = {
    # for local developement
    "name" : "$project_name",
    "version" : "",
    "description" : "",
    # for pypi
    "author" : "",
    "author_email" : "",
    "long_description" : "README.nf",
    "url" : "",
    "license" : "LICENSE.nf",
    "classifiers" : "", # See https://PyPI.python.org/PyPI?%3Aaction=list_classifier
    "keywords" : "",
    "include_package_data" : True,
    "package_data" : {},
    "entry_points" = {
        'console_scripts' : [],
    }
    "packages" : [find_packages(exclude=['docs', 'tests'])],
}
