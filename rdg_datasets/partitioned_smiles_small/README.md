test data for rdkit plugin.

this rdg is generated from the `smiles_small` rdg
to generate a new version of this rdg, first ensure a new version of `smiles_small` is available


## Manual generation steps

*These shouldn't be necessary as they are now in a script, use `./uprev` to generate a new version of this rdg*

then from this directory run:

1) `export NEW_VERSION=<new_storage_format_version>`
2) `mpirun -n 4 partition-dist --loadAllProperties --newRDG=$NEW_VERSION ../smiles_small/$NEW_VERSION` 

