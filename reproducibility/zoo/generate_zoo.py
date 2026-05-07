#!/usr/bin/env python3
"""Generate zoo from UCI/AllSet raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "zoo"
DEFAULT_RAW_DIR = Path("AllSet_all_raw_data") / DATASET_NAME
COL_NAMES = [
    "animal_name",
    "hair",
    "feathers",
    "eggs",
    "milk",
    "airborne",
    "aquatic",
    "predator",
    "toothed",
    "backbone",
    "breathes",
    "venomous",
    "fins",
    "legs",
    "tail",
    "domestic",
    "catsize",
    "type",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    data = pd.read_csv(raw_dir / "zoo.data", header=None)
    data.columns = COL_NAMES
    data = data.drop_duplicates(subset="animal_name", keep="first").reset_index(drop=True)
    data.insert(0, "node_id", range(1, len(data) + 1))

    edge_id = len(data) + 1
    edges = []
    edge_metadata = []
    for column in COL_NAMES[1:]:
        for value, rows in data.groupby(column):
            if value == "?":
                continue
            edges.append(rows["node_id"].tolist())
            edge_metadata.append({"name": f"{column}-{value}", "id": edge_id})
            edge_id += 1

    hypergraph = Hypergraph()
    hypergraph.add_nodes(
        node_list=data["node_id"].tolist(),
        metadata={
            int(row["node_id"]): {
                "animal_name": row["animal_name"],
                "class": int(row["type"]),
            }
            for _, row in data.iterrows()
        },
    )
    hypergraph.add_edges(edges, metadata=edge_metadata)
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
