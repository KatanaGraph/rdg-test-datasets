This graph is a 3 node graph: 3 self loops on one node, 9 self loops on another 
the other, and one node acting as a sink where the other 2 nodes have an outgoing edge
to it. "ai" suffix because it has filler labels, splits, and features.
The features in question are 2 length vectors: 1,1 for the self loop nodes and 
and 5,5 for the sink node.

The point of this file is to test arbitrary fan-out and different degree nodes during
sampling as well as in vs out-edge sampling (the sink node is ignored if you're sampling
in-edges).

# Generation

Use uprev to generate the graph (requires access to a katana_enterprise build). See the
top-level README for uprev instructions.
