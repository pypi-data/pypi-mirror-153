import os.path as osp

import yaml


def load_yaml(file_path, Loader=yaml.SafeLoader):
    """Load a YAML file into a Python dict.

    Parameters
    ----------
    file_path : str or pathlib.PosixPath
        The path to the YAML file.

    Returns
    -------
    data : dict
        A dict with the loaded yaml data.
    """
    if not osp.exists(str(file_path)):
        raise OSError('{} not exists'.format(str(file_path)))
    with open(osp.expanduser(file_path), 'r') as f:
        data = yaml.load(f, Loader=Loader)
    return data


def save_yaml(data, file_path):
    """Save a dict to a YAML file.

    Parameters
    ----------
    data : dict
        A dict with the loaded yaml data.
    file_path : str or pathlib.PosixPath
        The path to the YAML file.
    """
    with open(osp.expanduser(file_path), 'w') as f:
        yaml.dump(data, f, default_flow_style=None)
