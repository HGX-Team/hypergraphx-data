#!/usr/bin/env python3
"""Generate foodwebanalysis from the Florida Bay food-web raw files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "foodwebanalysis"
DEFAULT_RAW_DIR = Path("foodwebanalysis") / "raw"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "raw_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help="Directory containing Florida-bay-meta.csv and foodweb-hyper.csv.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def _parse_label(value: str) -> int | str:
    value = value.strip()
    return int(value) if value else ""


def read_node_metadata(raw_dir: Path) -> dict[int, dict[str, object]]:
    path = raw_dir / "Florida-bay-meta.csv"
    metadata: dict[int, dict[str, object]] = {}

    with path.open(newline="") as file_obj:
        reader = csv.reader(file_obj)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            node_id = int(row[0])
            metadata[node_id] = {
                "species": row[1],
                "label": _parse_label(row[2]),
            }

    return metadata


def read_hyperedges(raw_dir: Path) -> list[tuple[int, ...]]:
    path = raw_dir / "foodweb-hyper.csv"
    hyperedges: list[tuple[int, ...]] = []

    with path.open(newline="") as file_obj:
        for row in csv.reader(file_obj):
            if row:
                hyperedges.append(tuple(int(value) for value in row if value != ""))

    return hyperedges


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    node_metadata = read_node_metadata(raw_dir)
    hyperedges = read_hyperedges(raw_dir)

    hypergraph = Hypergraph()
    hypergraph.add_nodes(node_list=node_metadata.keys(), metadata=node_metadata)
    hypergraph.add_edges(edge_list=hyperedges)
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
