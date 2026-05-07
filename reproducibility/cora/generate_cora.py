#!/usr/bin/env python3
"""Generate cora from the AllSet coauthorship raw files."""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "cora"
DEFAULT_RAW_DIR = Path("AllSet_all_raw_data") / "coauthorship" / DATASET_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def sparse_feature_indices(row) -> list[int]:
    return [int(value) for value in row.nonzero()[1]]


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    labels = pickle.load((raw_dir / "labels.pickle").open("rb"))
    features = pickle.load((raw_dir / "features.pickle").open("rb"))
    raw_hypergraph = pickle.load((raw_dir / "hypergraph.pickle").open("rb"))

    nodes = list(
        range(
            min(min(edge) for edge in raw_hypergraph.values()),
            max(max(edge) for edge in raw_hypergraph.values()) + 1,
        )
    )
    node_metadata = {
        int(node): {
            "label": int(labels[index]),
            "features": sparse_feature_indices(features[index]),
        }
        for index, node in enumerate(nodes)
    }

    edge_metadata_by_edge: dict[tuple[int, ...], dict[str, object]] = {}
    for author, edge in raw_hypergraph.items():
        edge_key = tuple(sorted(int(node) for node in edge))
        metadata = edge_metadata_by_edge.setdefault(
            edge_key,
            {"label": [], "weight": 0},
        )
        metadata["label"].append(str(author))
        metadata["weight"] += 1

    hypergraph = Hypergraph()
    hypergraph.add_nodes(node_list=list(node_metadata), metadata=node_metadata)
    for edge, metadata in edge_metadata_by_edge.items():
        hypergraph.add_edge(edge, metadata=metadata)

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
