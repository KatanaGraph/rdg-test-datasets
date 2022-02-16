from __future__ import annotations

import os
import pathlib
import subprocess

from libuprev.uprev_config import Config
from libuprev import constants
from libuprev import fs

# create a new rdg by partitioning an existing rdg
# the input_rdg at the desired storage_format_version must already exist
def generate_partition_dist(config: Config,
                            input_rdg_path: pathlib.Path,
                            output_rdg_path: pathlib.Path,
                            storage_format_version: int,
                            num_partitions: int,
                            generate_args: list[str]
                            ) -> pathlib.Path:

    in_path = input_rdg_path / constants.STORAGE_FORMAT_VERSION_STR.format(storage_format_version)
    out_path = output_rdg_path / constants.STORAGE_FORMAT_VERSION_STR.format(storage_format_version)

    fs.ensure_dir("input rdg", in_path)
    fs.ensure_empty("output rdg", out_path)

    try:
        generate_partition_dist_tool(config=config,
                                     in_path=in_path,
                                     out_path=out_path,
                                     num_partitions=num_partitions,
                                     generate_args=generate_args)
    except:
        fs.cleanup(out_path)
        raise

    return out_path


def generate_partition_dist_tool(config: Config,
                                   in_path: pathlib.Path,
                                   out_path: pathlib.Path,
                                   num_partitions: int,
                                   generate_args: list[str],
                                   aws_disabled: bool = True):

    tool_name = "partition-dist"
    tool_path = (config.build_dir / constants.TOOLS.get(tool_name, None))

    fs.ensure_dir("build", config.build_dir)
    fs.ensure_file("generation_tool", tool_path, "have you built it?. Run 'make {}' in {}".format(tool_name, config.build_dir))

    # create command in the form "mpirun -n 4 partition-dist --SomeFlag --newRDG=<output_rdg_path> <input_rdg_path>
    cmd = ["mpirun", "-n", str(num_partitions), tool_path.absolute()] + generate_args + ["--newRDG={}".format(out_path.absolute()), in_path.absolute()]

    env = os.environ.copy()
    env["AWS_EC2_METADATA_DISABLED"] = str(aws_disabled)

    subprocess.run(cmd, check=True, env=env)
