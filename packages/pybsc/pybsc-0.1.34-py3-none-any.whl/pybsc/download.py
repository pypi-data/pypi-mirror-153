import re


valid = True
try:
    import urllib
    from urllib.request import urlopen
except ImportError:
    valid = False


def download_file(url, dst_path):
    """Download file from url.

    Parameters
    ----------
    url : str
        url.
    dst_path : str
        destination path.
    """
    if valid is False:
        raise RuntimeError('Not supported.')
    dst_path = str(dst_path)
    regex = r'[^\x00-\x7F]'
    matchedList = re.findall(regex, url)
    for m in matchedList:
        url = url.replace(m, urllib.parse.quote_plus(m, encoding="utf-8"))
    with urlopen(url) as web_file:
        data = web_file.read()
        with open(dst_path, mode='wb') as local_file:
            local_file.write(data)
