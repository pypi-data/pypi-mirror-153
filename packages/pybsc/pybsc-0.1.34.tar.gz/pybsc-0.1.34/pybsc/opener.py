import os.path as osp
import platform
import subprocess


def _open(filepath):
    pf = platform.system()
    if pf == 'Windows':
        opener = 'start'
    elif pf == 'Darwin':
        opener = 'open'
    else:
        opener = 'xdg-open'
    return '{opener} {filepath}'.format(opener=opener, filepath=filepath)


def opener(filepath):
    if not osp.exists(filepath):
        raise OSError('{} not exists'.format(filepath))
    proc = subprocess.Popen(
        _open(filepath),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True
    )
    proc.wait()
    return proc
