
def parse_sfv(rdg_storage_format_version: str) -> dict:
    components = rdg_storage_format_version.split(".")
    if len(components) < 2:
        raise RuntimeError("rdg_storage_format_version must have a <view identifier><storage_format_version> for each view type. If a view is not present, its storage_format_version should be 0. Ex: 'DLSG0.STPG9'")

    if not components == sorted(components):
        raise RuntimeError("rdg_storage_format_version view identifiers must be in alphabetical order")


    if "DLSG" not in components[0]:
        raise RuntimeError("no DLSG storage_format_version specified")

    if "STPG" not in components[1]:
        raise RuntimeError("no STPG storage_format_version specified")

    dlsg_sfv = int(components[0].replace("DLSG", ""))
    stpg_sfv = int(components[1].replace("STPG", ""))
    rdg_sfv_dict = {"dlsg": dlsg_sfv,
                    "stpg": stpg_sfv}

    return rdg_sfv_dict
