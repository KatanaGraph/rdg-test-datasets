This graph looks like the following:

    SEED  -S0-> ZERO     THREE <-S1- SEED
                |         |
                E0        E1
                |         |
                V         V
                ONE      FOUR
                |         |
                E2        E3
                |         |
                V         V
                TWO      FIVE

Each name above for the nodes above are node tags. The edges are also labeled
with edge tags. This graph is for testing heterogeneous export.

ai suffix because it has filler labels and splits. All nodes have labels 0,
and all node splits are 1 except for the seeds which
have split 0. It does NOT have features, so those will have to be added in
by the test.

# Generation

Use uprev to generate the graph (requires access to a katana_enterprise build). See the
top-level README for uprev instructions.
