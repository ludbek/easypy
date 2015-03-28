import re
import os

def get_abs_path(path):
    cwd = os.getcwd()
    if (re.match(r"./", path)):
        return '{}/{}'.format(cwd, path[2:])
    elif(re.match(r'^.$', path)):
        return cwd
    elif re.match(r"[^/]", path):
        return '{}/{}'.format(cwd, path)
    else:
        return path
