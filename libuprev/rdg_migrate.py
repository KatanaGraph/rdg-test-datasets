import os
import pathlib
import subprocess

from libuprev.uprev_config import Config
from libuprev import constants
from libuprev import fs


# create a new rdg by migrating from an rdg stored as a previous storage_format_version
# the input_rdg at in_ver must already exist
def migrate(config: Config,
            input_rdg_path: pathlib.Path,
            in_ver: int,
            out_ver: int
            )-> pathlib.Path:

    in_path = input_rdg_path / constants.STORAGE_FORMAT_VERSION_STR.format(in_ver)
    out_path = input_rdg_path / constants.STORAGE_FORMAT_VERSION_STR.format(out_ver)

    fs.ensure_dir("input rdg", in_path)
    fs.ensure_empty("output rdg", out_path)

    try:
        migrate_tool(config, in_path, out_path)
    except:
        fs.cleanup(out_path)
        raise

    return out_path


def migrate_tool(config: Config,
                     in_path: pathlib.Path,
                     out_path: pathlib.Path,
                     aws_disabled: bool = True):

    tool_name = "uprev-rdg-storage-format-version-worker"
    tool_path = (config.build_dir / constants.TOOLS.get(tool_name, None))

    fs.ensure_dir("build", config.build_dir)
    fs.ensure_file("migration_tool", tool_path, "have you built it?. Run 'make {}' in {}".format(tool_name, config.build_dir))

    # create command in the form "uprev-rdg-storage-format-version-worker <input_rdg> <output_rdg>"
    cmd = [tool_path.absolute(), in_path.absolute(), out_path.absolute()]

    env = os.environ.copy()
    env["AWS_EC2_METADATA_DISABLED"] = str(aws_disabled)
    subprocess.run(cmd, check=True, env=env)
