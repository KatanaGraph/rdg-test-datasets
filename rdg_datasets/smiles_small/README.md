test data for rdkit plugin.

The raw data from which the rdg is generated is in `csv_datasets/smiles_small/`

To generate this , follow these steps:
1) `export NEW_VERSION=<new_storage_format_version>`
2) `cd csv_datasets/smiles_small/;`
3) `csv-import  node_schema.txt edge_schema.txt ../../rdg_datasets/smiles_small/storage_format_version_$NEW_VERSION --ids-are-integers --files-have-headers`

TODO(emcginnis): make this an import script
