import os

from hypergraphx import Hypergraph, TemporalHypergraph


def load_simplex_with_metadata(dataset_path):
    """
    Load simplex data and node metadata, then store them in a Hypergraph.

    Parameters:
    - dataset_path (str): Path to the dataset files (directory containing the files).

    Returns:
    - Hypergraph: An instance of Hypergraph with loaded data and metadata.
    """
    # Define file paths
    nverts_file = os.path.join(dataset_path, "{}-nverts.txt".format(dataset_path))
    simplices_file = os.path.join(dataset_path, "{}-simplices.txt".format(dataset_path))
    times_file = os.path.join(dataset_path, "{}-times.txt".format(dataset_path))
    node_labels_file = os.path.join(
        dataset_path, "{}-node-labels.txt".format(dataset_path)
    )

    # Load data from files
    with open(nverts_file, "r") as f:
        nverts = [int(line.strip()) for line in f]

    with open(simplices_file, "r") as f:
        simplices = [int(line.strip()) for line in f]

    with open(times_file, "r") as f:
        times = [int(line.strip()) for line in f]

    with open(node_labels_file, "r") as f:
        node_labels = {}
        for line in f:
            node_id, author = line.strip().split(maxsplit=1)
            node_labels[int(node_id)] = {"class_name": author}

    # Check consistency
    if len(nverts) != len(times):
        raise ValueError(
            "The number of entries in nverts and times files must be the same."
        )

    if sum(nverts) != len(simplices):
        raise ValueError(
            "The sum of nverts must match the number of entries in simplices file."
        )

    # Create a Hypergraph instance
    hypergraph = Hypergraph()

    # Add all nodes and their metadata
    for node_id, metadata in node_labels.items():
        hypergraph.add_node(node=node_id, metadata=metadata)
    
    found_nodes = set()
    # Process and add edges to Hypergraph
    simplex_index = 0
    for i in range(len(nverts)):
        n = nverts[i]
        timestamp = times[i]

        simplex = tuple(simplices[simplex_index : simplex_index + n])
        for node in simplex:
            found_nodes.add(node)
        simplex_index += n

        hypergraph.add_edge(simplex)

    return hypergraph


def load_timestamped_simplex_with_metadata(dataset_path):
    """
    Load timestamped simplex data and node metadata, then store them in a TemporalHypergraph.

    Parameters:
    - dataset_path (str): Path to the dataset files (directory containing the files).

    Returns:
    - TemporalHypergraph: An instance of TemporalHypergraph with loaded data and metadata.
    """
    # Define file paths
    nverts_file = os.path.join(dataset_path, "{}-nverts.txt".format(dataset_path))
    simplices_file = os.path.join(dataset_path, "{}-simplices.txt".format(dataset_path))
    times_file = os.path.join(dataset_path, "{}-times.txt".format(dataset_path))
    node_labels_file = os.path.join(
        dataset_path, "{}-node-labels.txt".format(dataset_path)
    )
    simplex_labels_file = os.path.join(
        dataset_path, "{}-simplex-labels.txt".format(dataset_path)
    )

    # Load data from files
    with open(nverts_file, "r") as f:
        nverts = [int(line.strip()) for line in f]

    with open(simplices_file, "r") as f:
        simplices = [int(line.strip()) for line in f]

    with open(times_file, "r") as f:
        times = [int(line.strip()) for line in f]

    with open(simplex_labels_file, "r") as f:
        simplex_labels = [line.strip() for line in f]

    TIME_SHIFT = min(times)

    with open(node_labels_file, "r") as f:
        node_labels = {}
        for line in f:
            node_id, author = line.strip().split(maxsplit=1)
            node_labels[int(node_id)] = {"substance_name": author}

    

    # Check consistency
    if len(nverts) != len(times):
        raise ValueError(
            "The number of entries in nverts and times files must be the same."
        )

    if sum(nverts) != len(simplices):
        raise ValueError(
            "The sum of nverts must match the number of entries in simplices file."
        )

    # Process and add edges to TemporalHypergraph
    simplex_index = 0
    cont = 0
    un = {}
    for i in range(len(nverts)):
        cont+=1
        n = nverts[i]
        timestamp = times[i]

        # Extract the simplex (list of vertices)
        simplex = tuple(simplices[simplex_index : simplex_index + n])
        simplex_index += n
        label = simplex_labels[i]
        
        k = (timestamp, tuple(sorted(simplex)))
        if k in un:
            un[k].append(label)
        else:
            un[k] = [label]

    weighted = False
    for k in un:
        if len(un[k]) > 1:
            weighted = True
            break

    # Create a TemporalHypergraph instance
    temporal_hypergraph = TemporalHypergraph(weighted=weighted)

    # Add all nodes and their metadata
    for node_id, metadata in node_labels.items():
        temporal_hypergraph.add_node(node_id, metadata=metadata)

    # Add the simplex as an edge to the TemporalHypergraph

    for (timestamp, simplex) in un:
        label = un[(timestamp, simplex)]
        weight = len(label)
        temporal_hypergraph.add_edge(simplex, timestamp - TIME_SHIFT, weight=weight, metadata={"original_timestamp": timestamp, "label": label})
    
        
    return temporal_hypergraph


from hypergraphx.readwrite import save_hypergraph

if __name__ == "__main__":
    dataset_path = "NDC-classes-full"
    hypergraph = load_timestamped_simplex_with_metadata(dataset_path)
    hypergraph.set_attr_to_hypergraph_metadata("name", "NDC-classes")
    hypergraph.set_attr_to_hypergraph_metadata("version", "1.0.0")
    save_hypergraph(hypergraph, "NDC-classes.json")
    save_hypergraph(hypergraph, "NDC-classes.hgx", binary=True)

    from hypergraphx.readwrite import load_hypergraph
    a = load_hypergraph("NDC-classes.json")
    print(a.get_hypergraph_metadata())
    print(len(a.get_nodes()))
    print(len(a.get_edges()))
    b = load_hypergraph("NDC-classes.hgx")
    print(b.get_hypergraph_metadata())
    print(len(b.get_nodes()))
    print(len(b.get_edges()))
