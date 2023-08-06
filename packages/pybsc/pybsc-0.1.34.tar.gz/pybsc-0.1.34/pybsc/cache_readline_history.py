import atexit
import readline


def cache_readline(histfile, histlength=1000, emacs=True):
    try:
        readline.read_history_file(histfile)
        readline.set_history_length(histlength)
    except FileNotFoundError:
        pass
    if emacs is True:
        readline.parse_and_bind("set editing-mode emacs")
    atexit.register(readline.write_history_file, histfile)
