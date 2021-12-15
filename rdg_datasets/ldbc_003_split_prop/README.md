HOW THIS GRAPH WAS CREATED:


    1) in ParquetWriter.cpp change kMaxRowsPerFile to 10000
    ```
    constexpr int64_t kMaxRowsPerFile = 0x2710;
    ```

    2) remove the current ldbc_0003_split_prop

    2) re-import the graph, using the `csv-datasets` repo
    you will need to slightly modify the paths to match your system
    ```
    ./bin/csv-import --data-delimiter '|' --files-have-headers -t 32 --input-dir=/home/<user>/katana/katana-enterprise/external/csv-datasets/ldbc/ ~/katana/katana-enterprise/external/csv-datasets/ldbc/lists/nodes-sf-003-full.txt ~/katana/katana-enterprise/external/csv-datasets/ldbc/lists/edges-sf-003-full.txt ~/katana/katana-enterprise/external/rdg-test-inputs/ldbc_003_split_prop/
    ```

    it would be really nice if we could generate this in a more automated
    fashion, but this is the state of things as of now.
