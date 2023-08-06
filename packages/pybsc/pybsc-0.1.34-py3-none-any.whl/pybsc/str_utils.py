import string


printable = set(string.printable)


def removesuffix(s, suffix):
    return s[: -len(suffix)] if s.endswith(suffix) else s


def remove_non_ascii(s):
    return ''.join(filter(lambda x: x in printable, s))
