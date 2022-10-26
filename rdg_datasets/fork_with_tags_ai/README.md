This graph looks like the following:

    A0    A1    B0
    |     |     |
    E0    E1    G0
    |     |     |
    V     V     V
    A2    A3    B1
    |     |     |
    E2    G1   G2
     |    |    |
      |   |   |
       V  V  V
          C0
          |
          E3
          |
          V
          A4

Each letter is the tag. e.g., there are 5 nodes with tag A, 2 with tag B, one
with tag C.

All nodes have labels equivalent to the node ID, and all node splits are 1
except for the 3 at the top of the fork which have 0. It does NOT have
features, so those will have to be added in by the test.

# Generation

Use uprev to generate the graph (requires access to a katana_enterprise build). See the
top-level README for uprev instructions.
