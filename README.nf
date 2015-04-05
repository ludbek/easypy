WARNING
    this package is a protoype. it is created for sole purpose of exploring the
    possibilities of combining 'virtualenv', 'virtualenvwrapper', 'pip', 'invoke'
    and 'twine'.

HOW IT WORKS
    it uses 'invoke', the pythonic task executor at its core. it sits on top of
    'invoke', 'pip', 'virtualenv', 'virtualenvwrapper' and 'twine'. it provides
    tasks for creating and managing virtualenv, installing, removing, updating
    and automatically recording the package requirements at 'meta.json' file and
    finally registering and deploying python packages at 'pypi'.

AVAILABLE TASK
    GLOBAL
        start
            starts a new project. creates project directory at specified path,
            creates virtualenv for development. after the environment has been
            created one can work on it by issuing 'workon <project_name>' at the
            terminal.

            syntax:
                $ py start <project_name> -d <path/to/project/home/> [-p -f]
                options
                    -d = directory
                    -p = is it python package
                    -f = overwrite existing directory at project home
        end
            it removes virtual environments associated with a project. if --all
            option is specified it removes the  project directory as well.

            syntax
                $ py end <project_name> -a
                options
                    -a = if all, removes project directory as well
        setup
            set ups virtual environments for already existing project. the
            project must be created with easypy.

            syntax
                $ py setup [--test --dev --prod]
                options
                    --dev = for development environment
                    --test = for test environment
                    --prod = for production environment
        register
            it registers a python package at pypi. it uses 'python setup register'
            behind the scene.

            syntax
                $ py register

        deploy
            it bundles and uploads the python package to pypi.
            it uses 'python setup sdist' and 'twine upload dist/<package_dist_name>'

            syntax
                $ py deploy

    INSIDE VIRTUALENV
        add
            installs a python package and registers it as a requirements to the
            project. if an environment is not specified, it installs the package
            as common requirements for all the environments.

            syntax
                $ py add <package_name> [--dev --test --prod]
                options
                    --dev = installs in development environment
                    --test = installs in test environment
                    --prod = installs in production environment
        remove
            uninstalls a python package and removes it as a requirements to the
            project. for now an environment has to be specified.

            syntax
                $ py remove <package_name> [--dev --test --prod]
                options
                    --dev = installs in development environment
                    --test = installs in test environment
                    --prod = installs in production environment
        update
            updates a package. an environment has to be specified if the package
            is not a common requirement.

            syntax
                $ py update <package_name> [--dev --test --prod]
        meta
            displays and sets the meta information for a project.

            syntax
                $ py meta <property_name>[=property_value]

                available properties
                    - name
                    - version
                    - description