from __future__ import annotations

import os
import pathlib
import subprocess

from libuprev import constants, fs, rdg_sfv
from libuprev.uprev_config import Config


# create a new rdg by importing csv files
# named as such to avoid naming conflicts :(
def import_(
    config: Config,
    rdg_path: pathlib.Path,
    out_ver: str,
    csv_path: pathlib.Path,
    node_file: str,
    edge_file: str,
    import_args: list[str],
) -> pathlib.Path:

    rdg_sfv.parse_sfv(out_ver)

    out_path = rdg_path / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(out_ver)
    node_file_path = csv_path / node_file
    edge_file_path = csv_path / edge_file

    fs.ensure_empty("output rdg", out_path)
    fs.ensure_dir("csv", csv_path)
    fs.ensure_file("node", node_file_path)
    fs.ensure_file("edge", edge_file_path)

    # we want to maintain all of the possible rdg format views in the test-inputs
    import_args.append("--output-all-views")
    try:
        import_tool(config, out_path, csv_path, node_file_path, edge_file_path, import_args)
    except:
        fs.cleanup(out_path)
        raise

    return out_path


def import_tool(
    config: Config,
    out_path: pathlib.Path,
    input_dir: pathlib.Path,
    node_file_path: pathlib.Path,
    edge_file_path: pathlib.Path,
    import_args: list[str],
    aws_disabled: bool = True,
):

    tool_name = "csv-import"
    tool_path = config.build_dir / constants.TOOLS.get(tool_name, None)

    fs.ensure_dir("build", config.build_dir)
    fs.ensure_file(
        "import tool", tool_path, "have you built it?. Run 'make {}' in {}".format(tool_name, config.build_dir)
    )

    # create command in the form "csv-import  <node_file> <edge_file> <output_rdg_dir> <args>"
    cmd = [
        tool_path.absolute(),
        node_file_path.absolute(),
        edge_file_path.absolute(),
        out_path.absolute(),
        "--input-dir={}/".format(input_dir.absolute()),
    ] + import_args

    env = os.environ.copy()
    env["AWS_EC2_METADATA_DISABLED"] = str(aws_disabled)

    subprocess.run(cmd, check=True, env=env)
