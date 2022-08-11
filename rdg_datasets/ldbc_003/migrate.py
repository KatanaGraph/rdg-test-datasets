import os
import pathlib

from libuprev import rdg_migrate
from libuprev.uprev_config import Config

# vars unique to this rdg
local_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
input_rdg_storage_format_version = "DLSG0.STPG8"


def uprev(config: Config, new_rdg_storage_format_version: str) -> pathlib.Path:
    return rdg_migrate.migrate(config, local_path, input_rdg_storage_format_version, new_rdg_storage_format_version)
