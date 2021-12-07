import os
import pathlib
import shutil
import subprocess

from libuprev.uprev_config import Config


def migrate(config: Config, rdg_path: pathlib.Path, in_ver: int, out_ver: int) -> pathlib.Path:
    in_path = rdg_path / "storage_format_version_{}".format(in_ver)
    out_path = rdg_path / "storage_format_version_{}".format(out_ver)

    if not in_path.is_dir():
        raise RuntimeError("rdg must exist at {}".format(in_path))

    if out_path.is_dir() or out_path.is_file():
        raise RuntimeError("rdg must NOT already exist at {}".format(out_path))

    try:
        rdg_migrate_tool(config, in_path, out_path)
    except:
        if out_path.is_file():
            out_path.unlink()
        elif out_path.is_dir():
            shutil.rmtree(out_path)
        raise

    return out_path


def rdg_migrate_tool(config: Config, in_path: pathlib.Path, out_path: pathlib.Path):
    tool_path = (
        config.build_dir / "tools/uprev-rdg-storage-format-version-worker/uprev-rdg-storage-format-version-worker"
    )
    if tool_path == None:
        raise RuntimeError("path to migration tool must not be empty")
    if not tool_path.is_file():
        raise RuntimeError(
            "migration tool located at [{}] is not present, have you built it?".format(tool_path.absolute())
        )

    cmd = [tool_path, str(in_path.absolute()), str(out_path.absolute())]
    subprocess.run(cmd, check=True)
