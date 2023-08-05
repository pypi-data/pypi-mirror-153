import os
import sys

def which(program):
    """
    Returns the fully-qualified path to the specified binary
    """
    def is_exe(filepath):
        if sys.platform == 'win32':
            filepath = filepath.replace('\\', '/')
            for exe in [filepath, filepath + '.exe']:
                if all([os.path.isfile(exe), os.access(exe, os.X_OK)]):
                    return True
        else:
            return os.path.isfile(filepath) and os.access(filepath, os.X_OK)         
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None 