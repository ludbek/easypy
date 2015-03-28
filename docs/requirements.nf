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
                - view file 'templates/__meta__.py'
            inside setup.py
                - convert __meta__.meta dicts into proper setup() args
                - like read and parse file name mentioned in long_description, license, etc.

        Syntax
            $ py start <project-name> -d <directory-name> -f -p
            project-name : name of project
            directory-name
                - directory where project will reside
                - if not availabel it will look one at "PROJECT_HOME" enviroment \
                varialble
            -f : if a directory with requested project name exists \
            replace it(back it up)
            -p : it is a pythong package

            e.g.
                $ py start awesome-project
                $ py start awesome-project -d . -f

    2. meta.<meta_key>
        sets or gets the value of a meta key

        Syntax
        e.g.
            $ py meta.name [project-name] # set project name
            $ py meta.name  # get project name

    3. transform
        transforms a local module into a python package

    4. end
        ends a project, deletes its virtualenv, if specified removes the \
        project directory as well

        Syntax
            $ py end <project-name> -a
            project-name : name of the project
            -a, --all : remove project directory as well
    5. py
        lists help and tasks

        5.1. display easypy tasks
        Syntax: $ py

        5.2. display local tasks
        Syntax: $ py .

        5.3. display tasks in a package
        Syntax: $ py <package-name>

        5.4. display every tasks
        Syntax: $ py -a

note: USE REGEX TO MANIPULATE FILE?