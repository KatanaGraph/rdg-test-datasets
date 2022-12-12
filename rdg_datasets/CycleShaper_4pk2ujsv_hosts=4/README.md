This is a partitioned LSPG CycleShaper_4pk2ujsv graph (a synthetic graph) in format
DLSPG2.STPG0.  This is the only partitioned DLSPG2.STPG0 in the repository, so it is
useful for testing.  It has properties with many different types.

# Generation

The generate.py script generated the graph when run like this.

In one window run this

    scripts/dev run server --mount-gcp-credentials

In another run this

    scripts/dev pytest tools -v -s /source/external/katana/external/test-datasets/rdg_datasets/CycleShaper_4pk2ujsv_hosts=4/generate.py
    scripts/dev cp -r /build/storage_format_version_DLSG2.STPG0  storage_format_version_DLSG2.STPG0

Because the current (12/9/22) uprev framework only supports numeric graph
versions, we do not include any uprev/migration scripts.
