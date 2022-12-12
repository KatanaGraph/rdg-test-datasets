This is a partitioned LSPG rmat10 graph in format DLSPG1.STPG0.  This is the only
partitioned DLSPG1.STPG0 in the repository, so it is useful for testing.

# Generation

    ./dev tools _generic_import "rmat10" 6 --export-rdg

Which using the katana-tools dev, runs this script.

    https://github.com/KatanaGraph/katana-tools/blob/main/bench/katana_bench/importcsv.py

Because the current (12/9/22) uprev framework only supports numeric graph
versions, we do not include any uprev/migration scripts.

The generate.py script is much simpler than importcsv.py and it generates a valid
DLSPG2.STPG0 when run like this.

In one window run this

    scripts/dev run server --mount-gcp-credentials

In another run this

    scripts/dev pytest tools -v -s /source/external/katana/external/test-datasets/rdg_datasets/rmat10_hosts=6/generate.py
    scripts/dev cp -r /build/storage_format_version_DLSG2.STPG0  storage_format_version_DLSG2.STPG0
