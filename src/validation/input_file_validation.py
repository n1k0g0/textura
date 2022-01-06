import os.path


def is_valid_filename(fname):
    return os.path.isfile(fname)
