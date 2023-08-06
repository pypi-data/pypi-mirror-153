import os
import sys

import pyperclip


class ClipboardOutput(object):

    def __init__(self):
        self.buf = ''

    def write(self, arg):
        self.buf += arg


class stdout_to_clipboard(object):

    def __init__(self, print_stdout=True):
        sys.stdout.flush()
        self._org_stdout = sys.stdout
        self._old_stdout_fno = os.dup(sys.stdout.fileno())
        self._clip = ClipboardOutput()
        self.print_stdout = print_stdout

    def __enter__(self):
        sys.stdout = self._clip

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._org_stdout
        sys.stdout.flush()
        os.dup2(self._old_stdout_fno, 1)
        pyperclip.copy(self._clip.buf)
        if self.print_stdout:
            print(self._clip.buf)
