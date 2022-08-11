import pathlib
import shutil

from libuprev import constants


def ensure_file(name: str, path: pathlib.Path, message: str = None):
    if not path.is_file() and not path.is_char_device():
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

def ensure_exists(name: str, path: pathlib.Path, message: str = None):
    if not path.exists():
        if message is None:
            raise RuntimeError("{} does not exist at {}".format(name, path))
        else:
            raise RuntimeError("{} does not exist at {}: {}".format(name, path, message))

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


# TODO(emcginnis): it would be really really nice if we could easily detect these dependencies and resolve them automatically
# for now, this will have to do
def ensure_input_rdg_exists(input_rdg, input_rdg_path, rdg_storage_format_version: str):
    path = input_rdg_path / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(rdg_storage_format_version)
    error_message = "Creating this rdg depends on {0} at rdg_storage_format_version_{1}. First re-run this command with the flag '--rdg={0}. Once that completes, re-run the original command'".format(
        input_rdg, rdg_storage_format_version
    )
    ensure_dir("input rdg".format(input_rdg), path, error_message)


def ensure_build_dir(build_path: pathlib.Path):
    ensure_dir("katana-enterprise build directory", build_path)
    # use presence of CMakeCache.txt to determine if this is actually the build directory
    # this isn't perfect, but is used elsewhere in the codebase so is "good 'nuff"
    ensure_file(
        "cmake file",
        build_path / "CMakeCache.txt",
        "It doesn't look like the provided path is actually your build directory",
    )
