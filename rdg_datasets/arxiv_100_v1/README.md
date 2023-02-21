arxiv_100 is a small graph which has a fixedsizebinary vector feature for use in testing similarity graph construction.
It is extracted from the arxiv dataset that can be loaded/copied with:

python -m katana.ai.data.ogb_datasets --dataset arxiv

Then running the following queries on the resulting graph:

MATCH (a) WHERE id(a) > 99 DETACH DELETE a
MATCH ()-[b]->() DELETE b
MATCH (a) SET a:Node