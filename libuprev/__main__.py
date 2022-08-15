from __future__ import annotations

import glob
import json
import os
import pathlib
import shutil

import click
import flatbuffers
import rdg_datasets
from libuprev import color, constants, fs, tools, rdg_sfv, DistLogStructuredPropertyGraph
from libuprev.uprev_config import Config


def get_method(rdg: str, uprev_methods: dict):
    # Uprev Method Priority Order:
    # 1) Import
    # 2) Generate
    # 3) Migrate
    # Definitions of these three methods can be found in the repos root README.md
    if uprev_methods.get(rdg_datasets.import_method, None) != None:
        method = rdg_datasets.import_method
        method_handle = uprev_methods.get(rdg_datasets.import_method, None)

    elif uprev_methods.get(rdg_datasets.generate_method, None):
        method = rdg_datasets.generate_method
        method_handle = uprev_methods.get(rdg_datasets.generate_method, None)

    elif uprev_methods.get(rdg_datasets.migrate_method, None):
        method = rdg_datasets.migrate_method
        method_handle = uprev_methods.get(rdg_datasets.migrate_method, None)
    else:
        raise RuntimeError("no valid uprev method for rdg {}, available uprev methods {}".format(rdg, uprev_methods))

    return method, method_handle


def skip_uprev(rdg: str, rdg_storage_format_version: str, uprev_methods):
    method, method_handle = get_method(rdg, uprev_methods)
    path = method_handle.local_path / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(rdg_storage_format_version)
    if path.is_dir():
        return True, path
    return False, pathlib.Path


# Try to uprev the rdg using the available methods in priority order
# Returns path to upreved rdg
def try_uprev(config: Config, rdg: str, storage_format_version: int, uprev_methods: dict) -> pathlib.Path:
    method, method_handle = get_method(rdg, uprev_methods)
    color.print_ok(("Upreving rdg {}, using method [{}] found at [{}]".format(rdg, method, method_handle)))
    return method_handle.uprev(config, storage_format_version)

def validate_version(rdg: str, rdg_sfv_dict: dict, rdg_dir: pathlib.Path):
    fs.ensure_dir("rdg", rdg_dir)

    def validate_stpg_version(rdg:str, stpg_sfv: int, rdg_dir: pathlib.Path):
        globs = glob.glob(str(rdg_dir) + "/part_vers00000000000000000001_rdg*")
        if len(globs) == 0:
            raise RuntimeError("Failed to locate any static graph part headers for rdg {} in {}".format(rdg, rdg_dir))

        # arbitrarily choose the first one
        part_header_path = pathlib.Path(globs[0])
        if not part_header_path.is_file():
            raise RuntimeError("Failed to locate a valid static graph part header for rdg {}. Found globs : {}".format(rdg, globs))

        with open(part_header_path) as part_header:
            data = json.load(part_header)
            written_version = data.get("kg.v1.storage_format_version", None)
            if written_version == None:
                raise RuntimeError(
                    "rdg does not have storage_format_version in its static graph view part header. This is expected if this is a static graph view storage_format_version=1 rdg"
                )

            if written_version != stpg_sfv:
                raise RuntimeError(
                    "Written static graph view storage_format_version {} does not match expected the expected {}".format(
                        written_version, stpg_sfv
                    )
                )

    def validate_dlsg_version(rdg: str, dlsg_sfv: int, rdg_dir: pathlib.Path):
        globs = glob.glob(str(rdg_dir) + "/part_vers00000000000000000001_DLSPG*")
        if len(globs) == 0:
            raise RuntimeError("Failed to locate any DLSG part headers for rdg {} in {}".format(rdg, rdg_dir))

        # arbitrarily choose the first one
        part_header_path = pathlib.Path(globs[0])
        if not part_header_path.is_file():
            raise RuntimeError("Failed to locate a valid DLSG part header for rdg {}. Found globs : {}".format(rdg, globs))

        with open(part_header_path, "rb") as part_header:
            bbuf = bytearray(part_header.read())
            dlpg_part_header = DistLogStructuredPropertyGraph.DistLogStructuredPropertyGraph.GetRootAs(bbuf)
            written_version = dlpg_part_header.StorageFormatVersion()
            if written_version != dlsg_sfv:
                raise RuntimeError(
                    "Written DLSG graph view storage_format_version {} does not match expected the expected {}".format(
                        written_version, dlsg_sfv
                    )
                )

    validate_stpg_version(rdg, rdg_sfv_dict["stpg"], rdg_dir)
    if (rdg != "ldbc_003_maximal"):
        # skip validating the dlsg for ldbc_003_maximal
        validate_dlsg_version(rdg, rdg_sfv_dict["dlsg"], rdg_dir)

@click.group()
def cli():
    """
    tooling to uprev the test dataset rdgs to the latest rdg_storage_format_version

    the rdg_storage_format_version of an rdg is defined as an alphabetically ordered composite of each present views storage_format_version in the form
    <view1 identifer><view1 storage_format_version>.<view2 identifer><view2 storage_format_version>. etc
    ex:
    static graph storage_format_version = 9, which has the view identifer STPG
    lspg storage_format_version = 1, which has the view identifier DLSG
    rdg_storage_format_version = DLSG1.STPG9

    if a view is not present, its storage_format_version is 0
    ex:
    static graph storage_format_version = 9, which has the view identifer STPG
    and no lspg view
    rdg_storage_format_version = DLSG0.STPG9

    Only one views storage_format_version may be bumped during a single run of uprev
    To get from "DLSG1.STPG9" to "DLSPG2.STPG10" would require incrementing to either "DLSPG2.STPG9" or "DLSPG1.STPG10" first.

    to uprev all rdgs:
    uprev rdgs --storage_format_version="9-1" --build_dir="/home/user/katana-enterprise/build"

    to validate that all rdgs have a specific rdg_storage_format_version:
    uprev validate_rdgs --storage_format_version=9-1

    the --continue_on_failure flag can be used to skip over failures for individual rdgs, providing a report at the end

    --rdg=<rdg_name> or -R <rdg_name> can be passed to specify an rdg to work on
    this flag can be passed multiple times
    """


@cli.command(name="rdgs")
@click.option(
    "--rdg_storage_format_version",
    type=str,
    required=True,
    help="rdg_storage_format_version to uprev rdgs to. This should match the version which the in-tree tools will output and be of the form <view1 identifer><view1 storage_format_version>.<view2 identifer><view2 storage_format_version>. etc",
)
@click.option("--build_dir", type=str, required=True, help="katana-enterprise build directory")
@click.option(
    "--continue_on_failure", default=False, is_flag=True, help="Attempt to continue after exception", show_default=True
)
@click.option(
    "--rdg",
    "-R",
    "rdgs",
    type=str,
    multiple=True,
    help="RDG to operate on, can be passed multiple times: '-R ldbc_003 -R smiles_small'",
)
@click.option("--return_num_success", type=bool, default=False, hidden=True)
def cli_rdgs(
    rdg_storage_format_version: str, build_dir: str, continue_on_failure: bool, rdgs: list[str], return_num_success: bool
):
    rdg_sfv_dict = rdg_sfv.parse_sfv(rdg_storage_format_version)

    config = Config()
    config.build_dir = pathlib.Path(build_dir)
    fs.ensure_build_dir(config.build_dir)
    try:
        tools.in_tree_tools_built(config.build_dir)
    except Exception as e:
        raise RuntimeError(
            "Not all required tools are available, please run `./uprev build_tools --build_dir=<katana-enterprise build dir>`"
        )

    # mapping from the rdg that failed to the error received
    failed = {}
    # list of rdgs that must be manually upreved
    must_manually_uprev = []
    # mapping from the rdg that was successfully upreved, to its location
    uprev_success = {}
    # mapping of rdgs that have already been upreved, to their location
    skipped = {}

    if not set(rdgs).issubset(set(rdg_datasets.available_rdgs())):
        raise RuntimeError(
            "rdgs {} are not in the list of available rdgs \n\t Available rdgs: {}".format(
                rdgs, rdg_datasets.available_rdgs()
            )
        )

    for rdg, uprev_methods in rdg_datasets.available_uprev_methods().items():
        # skip over rdg if we have been passed a list to work on, and this is not one of them
        if len(rdgs) > 0 and rdg not in rdgs:
            continue

        if len(uprev_methods) == 0:
            must_manually_uprev.append(rdg)
            continue

        try:
            # skip over rdgs that are already at desired storage_format_version
            # still want to validate them though
            skip, path = skip_uprev(rdg, rdg_storage_format_version, uprev_methods)
            if not skip:
                uprev_success[rdg] = try_uprev(config, rdg, rdg_storage_format_version, uprev_methods)
                validate_version(rdg, rdg_sfv_dict, uprev_success[rdg])
                color.print_ok("Succeeded upreving {}".format(rdg))
            else:
                skipped[rdg] = path
                validate_version(rdg, rdg_sfv_dict, skipped[rdg])
                color.print_warn("Skipped upreving {}".format(rdg))

        except Exception as e:
            color.print_error("Failed upreving {}".format(rdg))
            if not continue_on_failure:
                raise
            else:
                failed[rdg] = e.args

    color.print_header(
        "**************************************** Uprev RDG Report ****************************************"
    )
    if len(skipped) > 0:
        color.print_warn(
            "******************** Skipped {} rdgs already at storage_format_version_{} ********************".format(
                len(skipped), rdg_storage_format_version
            )
        )
        for rdg, path in skipped.items():
            print("\t {} at {}".format(rdg, path))
        print()

    if len(uprev_success) > 0:
        color.print_ok(
            "******************** Successfully upreved {} rdgs ********************".format(len(uprev_success))
        )
        for rdg, path in uprev_success.items():
            print("\t {} at {}".format(rdg, path))
        print()

    if continue_on_failure and len(failed) > 0:
        color.print_error(
            "******************** Failed while trying to uprev the following {} rdgs ********************".format(
                len(failed)
            )
        )
        for rdg, reason in failed.items():
            print("\t {} : {}".format(rdg, reason))
        print()

    if len(must_manually_uprev) > 0:
        color.print_warn(
            "******************** Must manually uprev the following {} rdgs ********************".format(
                len(must_manually_uprev)
            )
        )
        color.print_warn("see the README file in the rdgs directory for manual uprev instructions")
        for rdg in must_manually_uprev:
            print("\t {1} at {0}/{1}/".format(rdg_datasets.rdg_dataset_dir, rdg))
        print()

    # used for testing
    if return_num_success:
        return len(uprev_success)


@cli.command(name="validate_rdgs")
@click.option(
    "--rdg_storage_format_version",
    type=str,
    required=True,
    help="rdg_storage_format_version to check. This should be of the form <view1 identifer><view1 storage_format_version>.<view2 identifer><view2 storage_format_version>. etc",
)
@click.option(
    "--continue_on_failure", default=False, is_flag=True, help="Attempt to continue after exception", show_default=True
)
@click.option(
    "--rdg",
    "-R",
    "rdgs",
    type=str,
    multiple=True,
    help="RDG to operate on, can be passed multiple times: '-R ldbc_003 -R smiles_small'",
)
def cli_validate_rdgs(rdg_storage_format_version: str, continue_on_failure: bool, rdgs: list[str]):

    rdg_sfv_dict = rdg_sfv.parse_sfv(rdg_storage_format_version)
    # mapping of the rdgs which were successfully validated, to its location
    validated_rdgs = {}
    # mapping from the rdg that failed to the error received
    failed = {}
    available_rdgs = rdg_datasets.available_rdgs()
    for rdg in available_rdgs:
        # skip over rdg if we have been passed a list to work on, and this is not one of them
        if len(rdgs) > 0 and rdg not in rdgs:
            continue

        rdg_dir = rdg_datasets.rdg_dataset_dir / rdg
        rdg_dir = rdg_dir / constants.RDG_STORAGE_FORMAT_VERSION_STR.format(rdg_storage_format_version)
        try:
            validate_version(rdg, rdg_sfv_dict, rdg_dir)
            validated_rdgs[rdg] = rdg_dir
        except Exception as e:
            if not continue_on_failure:
                raise
            else:
                failed[rdg] = e.args

    color.print_header(
        "**************************************** Validate RDG Report ****************************************"
    )
    if len(validated_rdgs) > 0:
        color.print_ok(
            "******************** Successfully validated {} rdgs ********************".format(len(validated_rdgs))
        )
        for rdg, path in validated_rdgs.items():
            print("\t {} at {}".format(rdg, path))
        print()

    if continue_on_failure and len(failed) > 0:
        color.print_error(
            "******************** Failed to validate the following {} rdgs ********************".format(len(failed))
        )
        for rdg, reason in failed.items():
            print("\t {} : {}".format(rdg, reason))
        print()

    if len(failed) == 0:
        num_should_validate = 0
        if len(rdgs) != 0:
            num_should_validate = len(rdgs)
        else:
            num_should_validate = len(available_rdgs)

        if num_should_validate != len(validated_rdgs):
            color.print_error("ERROR: not all available_rdgs were validated, but no failures were observed")
            print("expected to validate: {}".format(available_rdgs))
            print("but only validated: {}".format(validated_rdgs.keys()))


@cli.command(name="build_tools")
@click.option("--build_dir", type=str, required=True, help="katana-enterprise build directory")
def cli_build_tools(build_dir: str):
    build_path = pathlib.Path(build_dir)
    tools.build_in_tree_tools(build_path)


@cli.command(name="test")
@click.option(
    "--rdg_storage_format_version",
    type=str,
    required=True,
    help="rdg_storage_format_version to uprev rdgs to. This should match the version which the in-tree tools will output and be of the form <view1 identifer><view1 storage_format_version>.<view2 identifer><view2 storage_format_version>. etc",
)
@click.option("--build_dir", type=str, required=True, help="katana-enterprise build directory")
@click.pass_context
def cli_test(ctx, rdg_storage_format_version: int, build_dir: str):
    # assumes that the test rdgs are available at the passed storage_format_version already

    def cleanup(orig_paths: dict[str, pathlib.Path], backup_paths: dict[str, pathlib.Path]):
        for rdg, path in orig_paths.items():
            fs.cleanup(path)
        for rdg, path in backup_paths.items():
            shutil.move(path, rdg_paths.get(rdg, None))

    rdg_sfv_dict = rdg_sfv.parse_sfv(rdg_storage_format_version)

    # the rdgs to test upreving
    tests = {}
    tests[rdg_datasets.import_method] = "smiles_small"
    tests[rdg_datasets.generate_method] = "partitioned_smiles_small"
    tests[rdg_datasets.migrate_method] = "ldbc_003"

    available_rdgs = rdg_datasets.available_rdgs()
    available_methods = rdg_datasets.available_uprev_methods()

    tmp_path = pathlib.Path("/tmp")
    rdg_paths = {}
    backup_paths = {}
    rdg_storage_format_version_str = constants.RDG_STORAGE_FORMAT_VERSION_STR.format(rdg_storage_format_version)
    for method, rdg in tests.items():
        if rdg not in available_rdgs:
            raise RuntimeError("rdg {} to test {} on is not available".format(rdg, method))
        # store path of rdg at existing storage_format_version
        path = rdg_datasets.rdg_dataset_dir / rdg / rdg_storage_format_version_str
        fs.ensure_dir("rdg", path)
        rdg_paths[rdg] = path

        # store path to temporarily move the rdg to
        path = tmp_path / "{}_{}".format(rdg, rdg_storage_format_version_str)
        fs.ensure_empty("temp", path)
        backup_paths[rdg] = path

    # sanity check before we start
    ctx.invoke(cli_validate_rdgs, rdg_storage_format_version=rdg_storage_format_version, continue_on_failure=False)
    try:

        # move our test rdgs
        for method, rdg in tests.items():
            shutil.move(rdg_paths.get(rdg, None), backup_paths.get(rdg, None))

        # test import
        num_success = ctx.invoke(
            cli_rdgs,
            rdg_storage_format_version=rdg_storage_format_version,
            build_dir=build_dir,
            continue_on_failure=False,
            rdgs=[tests.get(rdg_datasets.import_method, None)],
            return_num_success=True,
        )
        if num_success != 1:
            raise RuntimeError("Expected to uprev 1 rdg, but instead upreved {}".format(num_success))

        # test upreving all uprev-able rdgs
        num_success = ctx.invoke(
            cli_rdgs,
            rdg_storage_format_version=rdg_storage_format_version,
            build_dir=build_dir,
            continue_on_failure=False,
            return_num_success=True,
        )
        if num_success != 2:
            raise RuntimeError("Expected to uprev 2 rdgs, but instead upreved {}".format(num_success))

        # ensure all rdgs are actually available again
        ctx.invoke(cli_validate_rdgs, rdg_storage_format_version=rdg_storage_format_version, continue_on_failure=False)

        # test running uprev when there is no work to do
        num_success = ctx.invoke(
            cli_rdgs,
            rdg_storage_format_version=rdg_storage_format_version,
            build_dir=build_dir,
            continue_on_failure=False,
            return_num_success=True,
        )
        if num_success != 0:
            raise RuntimeError("Expected to uprev 0 rdgs, but instead upreved {}".format(num_success))

        # ensure all is still sane
        ctx.invoke(cli_validate_rdgs, rdg_storage_format_version=rdg_storage_format_version, continue_on_failure=False)

    finally:
        cleanup(rdg_paths, backup_paths)
        ctx.invoke(cli_validate_rdgs, rdg_storage_format_version=rdg_storage_format_version, continue_on_failure=False)


if __name__ == "__main__":
    cli.main(prog_name="uprev")
