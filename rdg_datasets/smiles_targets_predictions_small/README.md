test data for HLS domain.

This graph has 3 node types Target, Compound and Bad_Compound, has a edge property: Target value and a node property: smiles. The graph is very similar to the rdg uses for HLS AI pipeline in Drug Target predictions. The old graphs `smiles_small` and `bad_smiles` do not allow testing functionalities on specific node types. Old graphs does not have edges property and node types and could not be split in 2 partitions without an empty node partition.

The raw data from which the rdg is generated is in `csv_datasets/smiles_targets_predictions_small/`

## Manual generation steps

*These shouldn't be necessary as they are now in a script, use `./uprev` to generate a new version of this rdg*

To generate this , follow these steps:
1) `export NEW_VERSION=<new_storage_format_version>`
2) `cd csv_datasets/smiles_targets_predictions_small/;`
3) `csv-import  node_schema.txt edge_schema.txt ../../rdg_datasets/smiles_targets_predictions_small/storage_format_version_$NEW_VERSION --ids-are-integers --files-have-headers`
