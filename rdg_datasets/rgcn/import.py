import os
import pathlib

import csv_datasets
from libuprev import rdg_import
from libuprev.uprev_config import Config

# vars unique to this rdg
local_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
csv_dataset = "rgcn"
csv_path = csv_datasets.csv_dataset_dir / csv_dataset
import_args = ["--ids-are-integers", "--files-have-headers", "--partition=random-oec"]
node_file = "node_schema.txt"
edge_file = "edge_schema.txt"


def uprev(config: Config, new_storage_format_version: int) -> pathlib.Path:
    available_csv = csv_datasets.available_csv()
    if csv_dataset not in available_csv:
        raise RuntimeError("csv dataset {} not in available csv_datasets: {}".format(csv_dataset, available_csv))

    return rdg_import.import_(
        config=config,
        rdg_path=local_path,
        out_ver=new_storage_format_version,
        csv_path=csv_path,
        node_file=node_file,
        edge_file=edge_file,
        import_args=import_args,
    )
