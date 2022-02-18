# Generating the empty graph

Currently the process I've used is to run csv-import on an empty file and change
the partition policy to 0.

TODO(aneesh): generate this from a script, or make it so that csv-import outputs
a valid graph with an empty set of nodes/edges
