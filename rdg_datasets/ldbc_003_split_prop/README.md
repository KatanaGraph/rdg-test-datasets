HOW THIS GRAPH WAS CREATED:


    1) in ParquetWriter.cpp change kMaxRowsPerFile to 10000
    ```
    constexpr int64_t kMaxRowsPerFile = 0x2710;
    ```

    2) remove the current ldbc_0003_split_prop

    2) re-import the graph, using the `csv-datasets` repo
    you will need to slightly modify the paths to match your system
    ```
    STORAGE_FORMAT_VERSION=storage_format_version_4
    DATASETS_PATH=${HOME}/katana/katana-enterprise/external/katana/external/test-datasets
    AWS_EC2_METADATA_DISABLED=true
    ./tools/import/csv-import --data-delimiter '|' --files-have-headers -t 32 --input-dir=${DATASETS_PATH}/csv_datasets/ldbc/ ${DATASETS_PATH}/csv_datasets/ldbc/lists/nodes-sf-003-full.txt ${DATASETS_PATH}/csv_datasets/ldbc/lists/edges-sf-003-full.txt ${DATASETS_PATH}/rdg_datasets/ldbc_003_split_prop/${STORAGE_FORMAT_VERSION}
    ```

    it would be really nice if we could generate this in a more automated
    fashion, but this is the state of things as of now.

    TODO(thunt): we could automate this with a feature flag for short parquet files.
