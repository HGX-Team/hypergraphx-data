#!/usr/bin/env python3
"""Generate Mushroom from AllSet/UCI raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "Mushroom"
DEFAULT_RAW_DIR = Path("AllSet_all_raw_data") / DATASET_NAME
ATTR_NAMES = [
    "cap-shape",
    "cap-surface",
    "cap-color",
    "bruises",
    "odor",
    "gill-attachment",
    "gill-spacing",
    "gill-size",
    "gill-color",
    "stalk-shape",
    "stalk-root",
    "stalk-surface-above-ring",
    "stalk-surface-below-ring",
    "stalk-color-above-ring",
    "stalk-color-below-ring",
    "veil-type",
    "veil-color",
    "ring-number",
    "ring-type",
    "spore-print-color",
    "population",
    "habitat",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def build_edges_and_metadata(raw_dir: Path) -> tuple[list[list[int]], list[dict[str, object]]]:
    data = pd.read_csv(raw_dir / "agaricus-lepiota.data", header=None)
    data[23] = data[0]
    data = data.drop([0], axis=1)

    groups = [
        (ATTR_NAMES[0:4], [1, 2, 3, 4]),
        (ATTR_NAMES[4:9], [5, 6, 7, 8, 9]),
        (ATTR_NAMES[9:15], [10, 11, 12, 13, 14, 15]),
        (ATTR_NAMES[15:20], [16, 17, 18, 19, 20]),
    ]
    edges = []
    metadata = []
    for names, columns in groups:
        for values, nodes in data.groupby(columns):
            if not isinstance(values, tuple):
                values = (values,)
            edges.append(sorted(nodes.index.tolist()))
            metadata.append({"|".join(names): list(values)})
    return edges, metadata


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    hyperedges, edge_metadata = build_edges_and_metadata(raw_dir)
    data = pd.read_csv(raw_dir / "agaricus-lepiota.data", header=None)
    data.columns = ["edibility"] + ATTR_NAMES
    data = data.drop(columns=["stalk-root"])
    node_metadata = data.T.to_dict()

    hypergraph = Hypergraph()
    hypergraph.add_nodes(node_list=list(node_metadata), metadata=node_metadata)
    for edge, metadata in zip(hyperedges, edge_metadata):
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
