This graph is a 2 node graph with 2 self loops on those nodes. "ai"
suffix because it has filler labels, splits, and features.
The features in question are 2 length vectors with 1 1 for the first node
and 2 2 for the second node

################################################################################
# Generation
################################################################################

Files used to generate this graph are in the generation directory.
The first part of this is generated from a csv, but the later part of it
requires running a script on the generated RDG. This is required because csv-import
doesn't support adding feature vectors.

First run csv-import from csv_datasets/two_self_loops_ai to get the topology:
./csv-import node_schema.txt  edge_schema.txt  two_self_loops_ai --ids-are-integers

After that, with the Katana distributed environment in Python path and the output RDG in
the same directory, run the add features script:
python3 add_features.py
