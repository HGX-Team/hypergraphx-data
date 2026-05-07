#!/usr/bin/env python3
"""Generate cat-edge-Cooking from Cornell/ARB categorical-edge raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "cat-edge-Cooking"
DEFAULT_RAW_DIR = Path(DATASET_NAME)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "raw_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help="Directory containing hyperedges.txt and hyperedge-labels.txt.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory where the generated .json and .hgx files are written.",
    )
    return parser.parse_args()


def read_hyperedges(path: Path) -> list[list[int]]:
    with path.open("r", encoding="utf-8") as file:
        return [list(map(int, line.split())) for line in file if line.strip()]


def read_labels(path: Path) -> list[int]:
    with path.open("r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file if line.strip()]


def read_label_identities(path: Path) -> dict[int, str]:
    with path.open("r", encoding="utf-8") as file:
        return {index + 1: line.strip() for index, line in enumerate(file) if line.strip()}


def read_node_labels(path: Path) -> dict[int, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        return {index + 1: label for index, line in enumerate(file) if (label := line.strip())}


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    hyperedges = read_hyperedges(raw_dir / "hyperedges.txt")
    edge_labels = read_labels(raw_dir / "hyperedge-labels.txt")
    edge_label_identities = read_label_identities(raw_dir / "hyperedge-label-identities.txt")
    node_labels = read_node_labels(raw_dir / "node-labels.txt")

    if len(hyperedges) != len(edge_labels):
        raise ValueError("hyperedges.txt and hyperedge-labels.txt have different sizes")

    hypergraph = Hypergraph()
    nodes_added = set()
    for edge, label_id in zip(hyperedges, edge_labels):
        for node in edge:
            if node in nodes_added:
                continue
            nodes_added.add(node)
            node_label = node_labels.get(node)
            if node_label:
                hypergraph.add_node(node, metadata={"name": node_label})
            else:
                hypergraph.add_node(node)

        edge_label = edge_label_identities.get(label_id)
        if edge_label:
            hypergraph.add_edge(edge, metadata={"label": edge_label})
        else:
            hypergraph.add_edge(edge)

    hypergraph.set_attr_to_hypergraph_metadata("name", DATASET_NAME)
    hypergraph.set_attr_to_hypergraph_metadata("version", "1.0.0")
    return hypergraph


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    hypergraph = build_hypergraph(args.raw_dir)

    json_path = args.output_dir / f"{DATASET_NAME}.json"
    hgx_path = args.output_dir / f"{DATASET_NAME}.hgx"
    save_hypergraph(hypergraph, str(json_path), fmt="json")
    save_hypergraph(hypergraph, str(hgx_path), fmt="pickle")

    for path in (json_path, hgx_path):
        loaded = load_hypergraph(str(path))
        print(f"{path}: nodes={len(loaded.get_nodes())} edges={len(loaded.get_edges())}")


if __name__ == "__main__":
    main()
