import os
import pathlib
import subprocess

import csv_datasets
from libuprev import constants, rdg_generate, rdg_import
from libuprev.uprev_config import Config

local_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
csv_dataset = "fork_with_tags_ai"
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

    return return_path
