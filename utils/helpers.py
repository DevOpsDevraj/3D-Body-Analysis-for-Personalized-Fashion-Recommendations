import os


def ensure_dir_exists(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return path
