import functools


# RGB order
flat_colors = {
    'red': (231, 76, 60),
    'blue': (52, 152, 219),
    'green': (46, 204, 113),
    'yellow': (241, 196, 15),
    'gray': (149, 165, 166),
    'silver': (189, 195, 199),
    'midnight_blue': (44, 62, 80),
    'purple': (142, 68, 173),
    'orange': (243, 156, 18),
    'turquoise': (26, 188, 156),
    'white': (245, 246, 250),
    'black': (47, 54, 64),
    'violet': (155, 89, 182),
    'brown': (93, 64, 55),
}


@functools.lru_cache(maxsize=None)
def _voc_colormap(i):
    r, g, b = 0, 0, 0
    for j in range(8):
        if i & (1 << 0):
            r |= 1 << (7 - j)
        if i & (1 << 1):
            g |= 1 << (7 - j)
        if i & (1 << 2):
            b |= 1 << (7 - j)
        i >>= 3
    return r, g, b


def voc_colormap(nlabels, order='rgb'):
    colors = []
    for i in range(nlabels):
        r, g, b = _voc_colormap(i)
        if order == 'rgb':
            colors.append([r, g, b])
        elif order == 'bgr':
            colors.append([b, g, r])
    return colors


def cmap(value):
    if isinstance(value, int):
        return _voc_colormap(value)
    if isinstance(value, str):
        return flat_colors[value]
    if isinstance(value, tuple):
        return value
