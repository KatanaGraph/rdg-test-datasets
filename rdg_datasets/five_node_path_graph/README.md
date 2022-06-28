This graph is a directed path graph containing five nodes, i.e., a chain of five nodes.

0 -> 1 -> 2 -> 3 -> 4

It has filler labels and splits that one can use it for ai purposes by adding features.
add_features scripts is not part of this dataset; one can refer to "add_features.py"
and "README.md" in "../two_self_loops_ai" to do similar.

The raw data from which the rdg is generated is in `csv_datasets/five_node_path_graph/`

################################################################################
# Generation
################################################################################

You can generate the topology by running csv-import from csv_datasets/five_node_path_graph.
`csv-import  node_schema.txt edge_schema.txt five_node_path_graph --ids-are-integers --files-have-headers`
