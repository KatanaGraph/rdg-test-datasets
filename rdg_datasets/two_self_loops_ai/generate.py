import os
import pathlib
import subprocess

import csv_datasets
from libuprev import rdg_import, constants, rdg_generate
from libuprev.uprev_config import Config

local_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
csv_dataset = "two_self_loops_ai"
csv_path = csv_datasets.csv_dataset_dir / csv_dataset
import_args = ["--ids-are-integers"]
node_file = "node_schema.txt"
edge_file = "edge_schema.txt"


def uprev(config: Config, new_storage_format_version: int) -> pathlib.Path:
    available_csv = csv_datasets.available_csv()
    if csv_dataset not in available_csv:
        raise RuntimeError("csv dataset {} not in available csv_datasets: {}".format(csv_dataset, available_csv))

    # imports topology first into an RDG
    return_path = rdg_import.import_(
        config=config,
        rdg_path=local_path,
        out_ver=new_storage_format_version,
        csv_path=csv_path,
        node_file=node_file,
        edge_file=edge_file,
        import_args=import_args,
    )

    # path to feature adding script in an enterprise build
    script_path = (
        config.build_dir / constants.TOOLS.get("katana_enterprise_python", None) / "python/test/datagen/two_self_loops_ai_features.py"
    )

    return rdg_generate.generate_python_enterprise_tool(config=config,
                                                        in_path=return_path,
                                                        out_path=None,
                                                        python_script_path=script_path, generate_args=[])
