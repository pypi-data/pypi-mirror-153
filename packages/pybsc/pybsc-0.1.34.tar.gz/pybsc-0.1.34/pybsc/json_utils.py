import json
import os.path as osp


def load_json(file_path, backend='builtin'):
    """Load json function.

    Parameters
    ----------
    file_path : str or pathlib.PosixPath
        json file path

    Returns
    -------
    data : dict
        loaded json data
    """
    if not osp.exists(str(file_path)):
        raise OSError('{} not exists'.format(str(file_path)))
    with open(str(file_path), "r") as f:
        if backend == 'builtin':
            return json.load(f)
        elif backend == 'orjson':
            import orjson
            return orjson.loads(f.read())
        else:
            raise NotImplementedError(
                "Not supported backend {}".format(backend))


def save_json(data, filename,
              save_pretty=True,
              sort_keys=True,
              ensure_ascii=True,
              backend='builtin'):
    """Save json function.

    Parameters
    ----------
    data : dict or list[dict]
        save data
    filename : str
        save path
    """
    filename = str(filename)
    if backend == 'builtin':
        with open(filename, "w") as f:
            if save_pretty:
                f.write(json.dumps(data, indent=4,
                                   ensure_ascii=ensure_ascii,
                                   sort_keys=sort_keys,
                                   separators=(',', ': ')))
            else:
                json.dump(data, f)
            f.write('\n')
    elif backend == 'orjson':
        import orjson
        with open(filename, "wb") as f:
            if save_pretty:
                f.write(orjson.dumps(
                    data,
                    option=orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2))
            else:
                f.write(orjson.dumps(data))
            f.write(b'\n')
    else:
        raise NotImplementedError("Not supported backend {}".format(backend))
