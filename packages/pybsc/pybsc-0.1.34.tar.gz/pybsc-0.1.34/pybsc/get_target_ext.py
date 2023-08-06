from collections import defaultdict
import os
import os.path as osp


def get_target_ext(base_path, exts):
    exts = tuple(exts)
    base_path = str(base_path)
    exts_dict = defaultdict(int)
    for ext in exts:
        exts_dict[ext] = 1
    for dirpath, _, files in os.walk(base_path):
        for f in files:
            _, ext = osp.splitext(f.lower())
            if exts_dict[ext]:
                yield os.path.join(dirpath, f)
