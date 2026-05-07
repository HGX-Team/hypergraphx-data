#!/usr/bin/env python3
"""Generate ModelNet40 from AllSet raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "ModelNet40"
DEFAULT_RAW_DIR = Path("AllSet_all_raw_data") / DATASET_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    content = np.genfromtxt(raw_dir / f"{DATASET_NAME}.content", dtype=np.dtype(str))
    labels = content[:, -1].astype(float)
    edge_node = pd.read_csv(
        raw_dir / f"{DATASET_NAME}.edges",
        sep=r"\s+",
        header=None,
        names=["edge_index", "node_index"],
    )
    hyperedges = (
        edge_node.groupby("edge_index")["node_index"]
        .agg(lambda values: sorted(set(values.tolist())))
        .tolist()
    )
    nodes = edge_node["node_index"].unique().tolist()
    node_metadata = {
        int(node): {"label": int(label)}
        for node, label in zip(nodes, labels[: len(nodes)])
    }

    hypergraph = Hypergraph()
    hypergraph.add_nodes(node_list=list(node_metadata), metadata=node_metadata)
    hypergraph.add_edges(edge_list=hyperedges)
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
