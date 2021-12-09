import pathlib
import subprocess
import os

from libuprev.uprev_config import Config
from libuprev import fs

# named as such to avoid naming conflicts :(
def import_(config: Config,
            rdg_path: pathlib.Path,
            out_ver: int,
            csv_path: pathlib.Path,
            node_file: str,
            edge_file: str,
            import_args: list[str]) -> pathlib.Path :

    out_path = rdg_path / "storage_format_version_{}".format(out_ver)
    node_file_path = csv_path / node_file
    edge_file_path = csv_path / edge_file

    fs.ensure_empty("output rdg", out_path)
    fs.ensure_dir("csv", csv_path)
    fs.ensure_file("node", node_file_path)
    fs.ensure_file("edge", edge_file_path)

    try:
        import_tool(config, out_path, csv_path, node_file_path, edge_file_path, import_args)
    except:
        fs.cleanup(out_path)
        raise

    return out_path



def import_tool(config: Config,
                out_path: pathlib.Path,
                input_dir: pathlib.Path,
                node_file_path: pathlib.Path,
                edge_file_path: pathlib.Path,
                import_args: list[str],
                aws_disabled: bool = True):
    tool_name = "csv-import"
    tool_path = (config.build_dir / "tools/import/{}".format(tool_name))

    fs.ensure_dir("build", config.build_dir)
    fs.ensure_file("import tool", tool_path, "have you built it?. Run 'make {}' in katana-enterprise".format(tool_name))

    cmd = [tool_path, node_file_path, edge_file_path, str(out_path.absolute()), "--input-dir={}/".format(input_dir)]
    cmd = cmd + import_args

    env = os.environ.copy()
    env["AWS_EC2_METADATA_DISABLED"] = str(aws_disabled)

    subprocess.run(cmd, check=True, env=env)
