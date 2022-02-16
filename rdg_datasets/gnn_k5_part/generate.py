import os
import pathlib

from libuprev import rdg_generate
from libuprev.uprev_config import Config
from libuprev import constants
from libuprev import fs
import rdg_datasets

# vars unique to this rdg
local_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
input_rdg = "gnn_k5_single"
input_rdg_path = rdg_datasets.rdg_dataset_dir / input_rdg
num_partitions = 2
generate_args = ["--partition=blocked-oec", "--mirrorEdges"]


def uprev(config: Config, new_storage_format_version: int) -> pathlib.Path:
    available_rdgs = rdg_datasets.available_rdgs()
    if input_rdg not in available_rdgs:
        raise RuntimeError("rdg dataset {} not available in rdg datasets: {}", input_rdg, available_rdgs)
    fs.ensure_input_rdg_exists(input_rdg, input_rdg_path, new_storage_format_version)
    return rdg_generate.generate_partition_dist(config=config,
                                                input_rdg_path=input_rdg_path,
                                                output_rdg_path=local_path,
                                                storage_format_version=new_storage_format_version,
                                                num_partitions=num_partitions,
                                                generate_args=generate_args)
