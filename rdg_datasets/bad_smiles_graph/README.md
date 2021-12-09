test data for rdkit plugin.

The raw data from which the rdg is generated is in `csv_datasets/bad_smiles/`


## Manual generation steps

*These shouldn't be necessary as they are now in a script, use `./uprev` to generate a new version of this rdg*

To generate this , follow these steps:
1) `export NEW_VERSION=<new_storage_format_version>`
2) `cd csv_datasets/bad_smiles/;`
3) `csv-import  node_schema.txt edge_schema.txt ../../rdg_datasets/bad_smiles_graph/storage_format_version_$NEW_VERSION --ids-are-integers --files-have-headers`
