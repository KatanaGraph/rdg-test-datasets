from __future__ import annotations

import os
import pathlib
import subprocess

from libuprev import constants, fs


def build_in_tree_tools(build_path: pathlib.Path):
    fs.ensure_build_dir(build_path)

    tools = list(constants.TOOLS.keys())
    do_build_(build_path, tools)

    try:
        in_tree_tools_built(build_path)
    except Exception as e:
        raise RuntimeError("not all tools are available after running make")


def in_tree_tools_built(build_path: pathlib.Path):
    for tool, path in constants.TOOLS.items():
        path = build_path / path
        fs.ensure_exists(tool, path)

def do_build_(build_path: pathlib.Path, tools: list[str]):
    cmd = ["make", "-j", str(os.cpu_count())] + tools
    subprocess.run(cmd, check=True, cwd=build_path)
