import os


def load_image_path(base_dir, filename):
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required image not found: {path}")
    return path
