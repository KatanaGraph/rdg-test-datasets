from katana import remote
from katana.remote import analytics, import_data, export_data


def repartition_to(client, in_path: str, out_path: str, num_partitions: int) :
    graph = client.create_graph()
    import_data.rdg(graph, in_path)
    graph.repartition(num_partitions=num_partitions)
    print(graph.num_nodes()) # Operation to force repartition
    export_data.rdg(graph, out_path)

    # Run via pytest
def test_repartition():
    # Connect to the Katana Server
    client = remote.Client()
    in_graph_path = "gs://katana-demo-datasets/synthetic/graphs/rdgs/CycleShaper_4pk2ujsv"
    out_graph_path = "/build/storage_format_version_DLSG2.STPG0"
    repartition_to(client, in_graph_path, out_graph_path, 4)

