def invert_dict(input_dict):
    """Inverrt key-value relationship in a dictionary

    Parameters
    ----------
    input_dict : dict
        input dictionary.
    """
    output_dict = {}
    for key, value in input_dict.items():
        output_dict[value] = key
    return output_dict
