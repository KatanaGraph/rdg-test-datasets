import os
import pathlib

import rdg_datasets
from libuprev import constants, fs, rdg_generate
from libuprev.uprev_config import Config

# vars unique to this rdg
local_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
input_rdg = "rgcn"
input_rdg_path = rdg_datasets.rdg_dataset_dir / input_rdg
num_partitions = 2
#TODO(emcginnis) we can't mirror edges on lspg
# generate_args = ["--partition=random-oec", "--mirrorEdges"]
generate_args = ["--partition=random-oec"]


def uprev(config: Config, new_rdg_storage_format_version: str) -> pathlib.Path:
    available_rdgs = rdg_datasets.available_rdgs()
    if input_rdg not in available_rdgs:
        raise RuntimeError("rdg dataset {} not available in rdg datasets: {}", input_rdg, available_rdgs)
    fs.ensure_input_rdg_exists(input_rdg, input_rdg_path, new_rdg_storage_format_version)
    return rdg_generate.generate_partition_dist(
        config=config,
        input_rdg_path=input_rdg_path,
        output_rdg_path=local_path,
        rdg_storage_format_version=new_rdg_storage_format_version,
        num_partitions=num_partitions,
        generate_args=generate_args,
    )

