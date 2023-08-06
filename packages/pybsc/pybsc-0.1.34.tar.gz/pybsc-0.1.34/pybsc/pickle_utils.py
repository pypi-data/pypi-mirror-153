import pickle


def load_pickle(file_path):
    """Load pickle data.

    Parameters
    ----------
    file_path : str or pathlib.PosixPath
        pickle file path
    """
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data
