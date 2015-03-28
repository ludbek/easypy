class TaskNotAvailable(Exception):
    def __init__(self, task):
        super(TaskNotAvailable, self).__init__("Task, %s is not available."%task)


class PackageNotAvailable(Exception):
    def __init__(self, task):
        super(PackageNotAvailable, self).__init__("Package, %s is not available."%task)

class TaskFailure(Exception):
    def __init__(self, message):
        super(TaskFailure, self).__init__(message)