Syntax
    1. $ py <package> , should list the tasks in a site package
    2. $ py , should list tasks in py
    3. $ py tasks , should list tasks in current project
    4. $ py <package> <atask>, should run a task in a package
    5. $ py <atask>, should run tasks in current project else in py

Tasks
    1. start
        starts a project, creates virtualenvs for the project
        initializes a project in following structure
            if not python package
                project-directory/
                    __init__.py
                    __meta__.py
            if python package
                project-directory/
                    setup.py
                    MANIFEST.in
                    LICENSE.txt
                    CHANGES.txt
                    README
                    package_name/
                        __init__.py
                        __meta__.py
            inside __meta__.py
                # https://tom-christie.github.io/articles/pypi/
                meta = {
                    # for local developement
                    'name' : <project name>,
                    'version' : <project version>,
                    'description' : <project description>,
                    'author' : <project owner>,
                    'author_email' : <owner email>,
                    'install_requires' : {
                        'common' : [],
                        'dev' : [],
                        'test' : [],
                        'prod' : []
                    }
                    # for pypi
                    'long_description' : '',
                    'url' : <project's home page>,
                    'license' : <project license",
                    'classifiers' : '', # See https://PyPI.python.org/PyPI?%3Aaction=list_classifier
                    'keywords' : <tags>,
                    'include_package_data' : True/False,
                    'package_data' : {},
                    'entry_points' = {
                        'console_scripts' : [],
                    }
                    'packages' : [],

                    ...
                }
            inside setup.py
                - convert __meta__.meta dicts into proper setup() args
                - like read and parse file name mentioned in long_description, license, etc.

        Syntax
            $py start <project-name> [-p]
            e.g.
                $ py start awesome_project
                $ py start . # if already in an empty project directory

    2. meta.<meta_key>
        sets or gets the value of a meta key

        Syntax
        e.g.
            $ py meta.name [project-name] # set project name
            $ py meta.name  # get project name

    3. transform
        trnsforms a local module into a python package

    4.terminate
        ends a project, deletes its virtualenv

note: USE REGEX TO MANIPULATE FILE?