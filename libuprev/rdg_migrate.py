import os
import pathlib
import subprocess

from libuprev import constants, fs, rdg_sfv
from libuprev.uprev_config import Config


# create a new rdg by migrating from an rdg stored as a previous storage_format_version
# the input_rdg at in_ver must already exist
def migrate(config: Config, input_rdg_path: pathlib.Path, in_ver: str, out_ver: str) -> pathlib.Path:

    rdg_sfv.parse_sfv(in_ver)
    rdg_sfv.parse_sfv(out_ver)

    in_path = input_rdg_path / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(in_ver)
    out_path = input_rdg_path / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(out_ver)

    fs.ensure_dir("input rdg", in_path)
    fs.ensure_empty("output rdg", out_path)

    try:
        migrate_tool(config, in_path, out_path)
    except:
        fs.cleanup(out_path)
        raise

    return out_path

def migrate_dist(config: Config, input_rdg_path: pathlib.Path, in_ver: str, out_ver: str, num_partitions:int) -> pathlib.Path:
    rdg_sfv.parse_sfv(in_ver)
    rdg_sfv.parse_sfv(out_ver)

    in_path = input_rdg_path / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(in_ver)
    out_path = input_rdg_path / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(out_ver)

    fs.ensure_dir("input rdg", in_path)
    fs.ensure_empty("output rdg", out_path)

    try:
        migrate_dist_tool(config, in_path, out_path, num_partitions)
    except:
        fs.cleanup(out_path)
        raise

    return out_path


def migrate_tool(config: Config, in_path: pathlib.Path, out_path: pathlib.Path, aws_disabled: bool = True):

    tool_name = "uprev-rdg-storage-format-version-dist-worker"
    tool_path = config.build_dir / constants.TOOLS.get(tool_name, None)

    fs.ensure_dir("build", config.build_dir)
    fs.ensure_file(
        "migration_tool", tool_path, "have you built it?. Run 'make {}' in {}".format(tool_name, config.build_dir)
    )

    # create command in the form "uprev-rdg-storage-format-version-dist-worker <input_rdg> <output_rdg>"
    cmd = [tool_path.absolute(), in_path.absolute(), out_path.absolute()]

    env = os.environ.copy()
    env["AWS_EC2_METADATA_DISABLED"] = str(aws_disabled)
    subprocess.run(cmd, check=True, env=env)

def migrate_dist_tool(config: Config, in_path: pathlib.Path, out_path: pathlib.Path, num_partitions: int, aws_disabled: bool = True):

    tool_name = "uprev-rdg-storage-format-version-dist-worker"
    tool_path = config.build_dir / constants.TOOLS.get(tool_name, None)

    fs.ensure_dir("build", config.build_dir)
    fs.ensure_file(
        "migration_tool", tool_path, "have you built it?. Run 'make {}' in {}".format(tool_name, config.build_dir)
    )

    # create command in the form "mpirun -n 4 uprev-rdg-storage-format-version-dist-worker <input_rdg> <output_rdg>"
    cmd = ["mpirun", "-n", str(num_partitions), tool_path.absolute(), in_path.absolute(), out_path.absolute() ]

    env = os.environ.copy()
    env["AWS_EC2_METADATA_DISABLED"] = str(aws_disabled)
    subprocess.run(cmd, check=True, env=env)
