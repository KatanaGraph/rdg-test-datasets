from __future__ import annotations

import os
import pathlib

csv_dataset_dir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))


def available_csv() -> list[str]:
    dirs = os.walk(csv_dataset_dir)
    subdirs = next(dirs)[1]

    # clear unavoidable garbage directories
    subdirs.remove("__pycache__")
    return subdirs
