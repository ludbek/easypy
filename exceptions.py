class TaskNotAvailable(Exception):
    def __init__(self, task):
        super(TaskNotAvailable, self).__init__("Task, %s is not available."%task)


class PackageNotAvailable(Exception):
    def __init__(self, task):
        super(PackageNotAvailable, self).__init__("Package, %s is not available."%task)

class InvalidPackage(Exception):
    def __init__(self, package_name):
        super(InvalidPackage, self).__init__("Package, %s does not have valid tasks for easypy."%package_name)

class TaskFailure(Exception):
    def __init__(self, message):
        super(TaskFailure, self).__init__(message)

class PackageAlreadyInstalled(Exception):
    def __init__(self, package):
        super(PackageAlreadyInstalled, self).__init__("Package, {0} has already been installed.".format(package))
