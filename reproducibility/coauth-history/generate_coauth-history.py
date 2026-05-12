#!/usr/bin/env python3
"""Generate coauth-history from local simplex raw files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from hypergraphx import Hypergraph, TemporalHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "coauth-history"
DEFAULT_RAW_DIR = Path("coauth-MAG-History-full")


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

    edge_labels_present = True
    try:
        with open(simplex_labels_file, "r") as f:
            simplex_labels = [line.strip() for line in f]
    except FileNotFoundError:
        edge_labels_present = False

    TIME_SHIFT = min(times)

    with open(node_labels_file, "r") as f:
        node_labels = {}
        for line in f:
            node_id, author = line.strip().split(maxsplit=1)
            node_labels[int(node_id)] = {"author": author}

    

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

        if edge_labels_present:
            label = simplex_labels[i]
        else:
            label = False          
        
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
        if weighted:
            weight = len(label)
        else:
            weight = None
        
        if False not in label:
            temporal_hypergraph.add_edge(simplex, timestamp - TIME_SHIFT, weight=weight, metadata={"original_timestamp": timestamp, "paper_title": label})
        else:
            temporal_hypergraph.add_edge(simplex, timestamp - TIME_SHIFT, weight=weight, metadata={"original_timestamp": timestamp})
    
        
    return temporal_hypergraph


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def save_and_validate(hypergraph, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{DATASET_NAME}.json"
    hgx_path = output_dir / f"{DATASET_NAME}.hgx"
    save_hypergraph(hypergraph, str(json_path), fmt="json")
    save_hypergraph(hypergraph, str(hgx_path), fmt="pickle")
    for path in (json_path, hgx_path):
        loaded = load_hypergraph(str(path))
        print(f"{path}: nodes={len(loaded.get_nodes())} edges={len(loaded.get_edges())}")


def main() -> None:
    args = parse_args()
    hypergraph = load_timestamped_simplex_with_metadata(str(args.raw_dir))
    hypergraph.set_attr_to_hypergraph_metadata("name", DATASET_NAME)
    hypergraph.set_attr_to_hypergraph_metadata("version", "1.0.0")
    save_and_validate(hypergraph, args.output_dir)


if __name__ == "__main__":
    main()
