import os
import sys


class suppress_stdout(object):

    """A context manager that block stdout for its scope

    with HideOutput():
        os.system('ls -l')

    From https://stackoverflow.com/a/17954769/4176597

    """

    def __init__(self, to=os.devnull):
        sys.stdout.flush()
        self._org_stdout = sys.stdout
        self._old_stdout_fno = os.dup(sys.stdout.fileno())
        self._to = os.open(to, os.O_WRONLY)

    def __enter__(self):
        self._newstdout = os.dup(1)
        os.dup2(self._to, 1)
        os.close(self._to)
        sys.stdout = os.fdopen(self._newstdout, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._org_stdout
        sys.stdout.flush()
        os.dup2(self._old_stdout_fno, 1)
