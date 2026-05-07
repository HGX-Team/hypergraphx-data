#!/usr/bin/env python3
"""Generate coauth-cs-ICML from the cat-edge-MAG-10 raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

from hypergraphx import Hypergraph, MultiplexHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "coauth-cs-ICML"
TARGET_LABEL = 'ICML'
IS_MULTIPLEX = False
DEFAULT_RAW_DIR = Path("cat-edge-MAG-10")
SKIP_LABEL = 67279


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


def read_label_identities(path: Path) -> dict[int, str]:
    with path.open("r", encoding="utf-8") as file:
        return {index + 1: line.strip() for index, line in enumerate(file) if line.strip()}


def build_hypergraph(raw_dir: Path):
    hyperedges = read_hyperedges(raw_dir / "hyperedges.txt")
    edge_labels = read_ints(raw_dir / "hyperedge-labels.txt")
    label_by_id = read_label_identities(raw_dir / "hyperedge-label-identities.txt")
    id_by_label = {label: label_id for label_id, label in label_by_id.items()}

    if len(hyperedges) != len(edge_labels):
        raise ValueError("hyperedges.txt and hyperedge-labels.txt have different sizes")

    if IS_MULTIPLEX:
        hypergraph = MultiplexHypergraph()
        nodes_added = set()
        for edge, label_id in zip(hyperedges, edge_labels):
            if label_id == SKIP_LABEL:
                continue
            for node in edge:
                if node not in nodes_added:
                    nodes_added.add(node)
                    hypergraph.add_node(node)
            hypergraph.add_edge(edge, layer=label_id)
    else:
        if TARGET_LABEL not in id_by_label:
            raise ValueError(f"{TARGET_LABEL!r} is not present in hyperedge-label-identities.txt")
        target_id = id_by_label[TARGET_LABEL]
        hypergraph = Hypergraph()
        nodes_added = set()
        for edge, label_id in zip(hyperedges, edge_labels):
            if label_id != target_id or label_id == SKIP_LABEL:
                continue
            for node in edge:
                if node not in nodes_added:
                    nodes_added.add(node)
                    hypergraph.add_node(node)
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
