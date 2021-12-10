import os
import pathlib
import subprocess

from libuprev import constants, fs

def build_in_tree_tools(build_path: pathlib.Path):
    fs.ensure_build_dir(build_path)

    tools = list(constants.TOOLS.keys())
    do_build_(build_path, tools)
    if not in_tree_tools_built(build_path):
        raise RuntimeError("not all tools are built after running make")

def in_tree_tools_built(build_path: pathlib.Path):
    for tool, path in constants.TOOLS.items():
        path = build_path / path
        try:
            fs.ensure_file(tool, path)
        except:
            return False

    return True

def do_build_(build_path: pathlib.Path, tools: list[str]):
    cmd = ["make", "-j", str(os.cpu_count())] + tools
    subprocess.run(cmd, check=True, cwd=build_path)
