from katana_enterprise import distributed
from katana.distributed import Graph

import pyarrow
import numpy as np

distributed.initialize()

features_numpy = np.array([[1, 1], [2, 2]], np.float32)
features_numpy = np.ascontiguousarray(features_numpy)

# dist prop graph
print("Loading RDG", flush=True)
original_graph = Graph("two_self_loops_ai")

print("rdg loaded",flush=True)

number_of_nodes = original_graph.num_nodes()
assert number_of_nodes == features_numpy.shape[0]

# the total number of bytes in a feature vector of a node
pa_type = pyarrow.binary(features_numpy.dtype.itemsize * features_numpy.shape[1])
arrow_buffer = pyarrow.py_buffer(features_numpy.data)
buffers = [None, arrow_buffer]
# creates pyarrow wrapper over the numpy array
pyarrow_array = pyarrow.Array.from_buffers(pa_type, number_of_nodes, buffers=buffers)

print("craeted pyarrow array",flush=True)

# to table
table = pyarrow.Table.from_arrays([pyarrow_array], ["feature"])
# save to in-memory graph
original_graph.upsert_node_property(table)

print("Begin write via commit",flush=True)
# commit: this is an in place operation
original_graph.write()
