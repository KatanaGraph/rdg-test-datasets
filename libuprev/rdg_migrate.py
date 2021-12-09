import os
import pathlib
import subprocess

from libuprev.uprev_config import Config
from libuprev import fs


def migrate(config: Config,
            rdg_path: pathlib.Path,
            in_ver: int,
            out_ver: int
            )-> pathlib.Path:

    in_path = rdg_path / "storage_format_version_{}".format(in_ver)
    out_path = rdg_path / "storage_format_version_{}".format(out_ver)

    fs.ensure_dir("rdg", in_path)
    fs.ensure_empty("rdg", out_path)

    try:
        rdg_migrate_tool(config, in_path, out_path)
    except:
        fs.cleanup(out_path)
        raise

    return out_path


def rdg_migrate_tool(config: Config,
                     in_path: pathlib.Path,
                     out_path: pathlib.Path,
                     aws_disabled: bool = True):

    tool_name = "uprev-rdg-storage-format-version-worker"
    tool_path = (
        config.build_dir / "external/katana/tools/{0}/{0}".format(tool_name)
    )
    fs.ensure_dir("build", config.build_dir)
    fs.ensure_file("migration_tool", tool_path, "have you built it?. Run 'make {}' in katana-enterprise".format(tool_name))

    cmd = [tool_path, str(in_path.absolute()), str(out_path.absolute())]

    env = os.environ.copy()
    env["AWS_EC2_METADATA_DISABLED"] = str(aws_disabled)
    subprocess.run(cmd, check=True, env=env)
