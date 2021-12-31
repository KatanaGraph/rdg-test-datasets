import os
import pathlib

from libuprev import rdg_migrate
from libuprev.uprev_config import Config

# vars unique to this rdg
local_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
input_storage_format_version = 3


def uprev(config: Config, new_storage_format_version: int) -> pathlib.Path:
    return rdg_migrate.migrate(config, local_path, input_storage_format_version, new_storage_format_version)
