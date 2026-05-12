#!/usr/bin/env python3
"""Generate house-committees from local ARB raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "house-committees"
DEFAULT_RAW_DIR = Path(DATASET_NAME)


def load_hyperedges(raw_dir: Path):
    path = raw_dir / f"hyperedges-{DATASET_NAME}.txt"
    hyperedges = {}
    weighted = False
    with open(path) as f:
        for line in f:
            h = tuple(sorted(map(int, line.strip().split(','))))
            if h not in hyperedges:
                hyperedges[h] = 0
            hyperedges[h] += 1
            if hyperedges[h] > 1:
                weighted = True
    
    return hyperedges, weighted


def load_nodes(raw_dir: Path):
    path1 = raw_dir / f"label-names-{DATASET_NAME}.txt"
    path2 = raw_dir / f"node-labels-{DATASET_NAME}.txt"
    path3 = raw_dir / f"node-names-{DATASET_NAME}.txt"

    f = open(path1, "r")
    labels = f.readlines()
    f.close()
    f = open(path2, "r")
    node_labels = f.readlines()
    f.close()
    f = open(path3, "r")
    node_names = f.readlines()
    f.close()

    id2label = {}
    for i in range(len(labels)):
        id2label[i+1] = labels[i].strip()

    nodes = {}

    for i in range(len(node_names)):
        nodes[i+1] = {
            "name": node_names[i].strip(),
            "label": id2label[int(node_labels[i].strip())]
        }

    return nodes


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    h, w = load_hyperedges(raw_dir)
    n = load_nodes(raw_dir)

    hypergraph = Hypergraph(weighted=w)

    for node in n:
        hypergraph.add_node(node, metadata=n[node])

    for hyperedge in h:
        if w:
            hypergraph.add_edge(hyperedge, weight=h[hyperedge])
        else:
            hypergraph.add_edge(hyperedge)

    return hypergraph


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def save_and_validate(hypergraph: Hypergraph, output_dir: Path) -> None:
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
    hypergraph = build_hypergraph(args.raw_dir)
    hypergraph.set_attr_to_hypergraph_metadata("name", DATASET_NAME)
    hypergraph.set_attr_to_hypergraph_metadata("version", "1.0.0")
    save_and_validate(hypergraph, args.output_dir)


if __name__ == "__main__":
    main()
