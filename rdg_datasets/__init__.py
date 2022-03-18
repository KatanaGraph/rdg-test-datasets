from __future__ import annotations

import importlib
import os
import pathlib
import sys

rdg_dataset_dir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
migrate_method = "migrate"
generate_method = "generate"
import_method = "import"

# This function attempts to provide flexibility and avoid hardcoding the specific RDGs / uprev methods used
# 1) Ensure any added RDGs are automatically found
# 2) Ensure that no matter the uprev method used, assuming it follows proper naming conventions, it is found
# 3) Ensure we are aware of RDGs missing automated uprev methods


def available_rdgs() -> list[str]:
    dirs = os.walk(rdg_dataset_dir)
    subdirs = next(dirs)[1]

    # clear unavoidable garbage directories
    subdirs.remove("__pycache__")
    return subdirs


def available_uprev_methods():
    # Definitions of these three methods can be found in the repos root README.md
    conditional_methods = [generate_method, migrate_method, import_method]

    subdirs = available_rdgs()
    available_uprev_methods = {}

    # go through all of the subdirectories and locate modules that implement one of the conditional_methods
    for dir in subdirs:
        available_uprev_methods[dir] = {}
        for method in conditional_methods:
            try:
                method_handle = importlib.import_module("{}.{}".format(dir, method))
                available_uprev_methods[dir][method] = method_handle

            except ModuleNotFoundError as e:
                pass
            # print("unable to find {} method for {}, {}".format(method, dir, e.msg))

    return available_uprev_methods
