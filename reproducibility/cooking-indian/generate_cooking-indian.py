#!/usr/bin/env python3
"""Generate cooking-indian from the cat-edge-Cooking raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

from hypergraphx import Hypergraph, MultiplexHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "cooking-indian"
TARGET_LABEL = 'indian'
IS_MULTIPLEX = False
DEFAULT_RAW_DIR = Path("cat-edge-Cooking")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def read_hyperedges(path: Path) -> list[list[int]]:
    with path.open("r", encoding="utf-8") as file:
        return [list(map(int, line.split())) for line in file if line.strip()]


def read_ints(path: Path) -> list[int]:
    with path.open("r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file if line.strip()]


def read_lines(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def build_hypergraph(raw_dir: Path):
    hyperedges = read_hyperedges(raw_dir / "hyperedges.txt")
    edge_labels = read_ints(raw_dir / "hyperedge-labels.txt")
    label_by_id = {index + 1: label for index, label in enumerate(read_lines(raw_dir / "hyperedge-label-identities.txt"))}
    id_by_label = {label: label_id for label_id, label in label_by_id.items()}
    node_labels = {index + 1: label for index, label in enumerate(read_lines(raw_dir / "node-labels.txt")) if label}

    if len(hyperedges) != len(edge_labels):
        raise ValueError("hyperedges.txt and hyperedge-labels.txt have different sizes")

    if IS_MULTIPLEX:
        hypergraph = MultiplexHypergraph()
        nodes_added = set()
        for edge, label_id in zip(hyperedges, edge_labels):
            for node in edge:
                if node not in nodes_added:
                    nodes_added.add(node)
                    metadata = {"name": node_labels[node]} if node in node_labels else None
                    hypergraph.add_node(node, metadata=metadata)
            hypergraph.add_edge(edge, layer=label_id)
    else:
        if TARGET_LABEL not in id_by_label:
            raise ValueError(f"{TARGET_LABEL!r} is not present in hyperedge-label-identities.txt")
        target_id = id_by_label[TARGET_LABEL]
        hypergraph = Hypergraph()
        nodes_added = set()
        for edge, label_id in zip(hyperedges, edge_labels):
            if label_id != target_id:
                continue
            for node in edge:
                if node not in nodes_added:
                    nodes_added.add(node)
                    metadata = {"name": node_labels[node]} if node in node_labels else None
                    hypergraph.add_node(node, metadata=metadata)
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
