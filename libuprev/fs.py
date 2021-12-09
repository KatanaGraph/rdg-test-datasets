import pathlib
import shutil

def ensure_file(name: str, path: pathlib.Path, message: str = None):
    if not path.is_file():
        if message is None:
            raise RuntimeError("{} file does not exist at {}".format(name, path))
        else:
            raise RuntimeError("{} file does not exist at {}: {}".format(name, path, message))



def ensure_dir(name: str, path: pathlib.Path, message: str = None):
    if not path.is_dir():
        if message is None:
            raise RuntimeError("{} directory does not exist at {}".format(name, path))
        else:
            raise RuntimeError("{} directory does not exist at {}: {}".format(name, path, message))


def ensure_empty(name: str, path: pathlib.Path, message: str = None):
    if path.exists():
        if message is None:
            raise RuntimeError("{} already exists at {}".format(name, path))
        else:
            raise RuntimeError("{} already exists at {}: ".format(name, path, message))

def cleanup(path: pathlib.Path):
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
