#!/usr/bin/env python3
"""Generate walmart-trips from Cornell/ARB node-labeled hypergraph raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "walmart-trips"
DEFAULT_RAW_DIR = Path(DATASET_NAME)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "raw_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help="Raw dataset directory containing hyperedges, node labels, and label names files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory where the generated .json and .hgx files are written.",
    )
    return parser.parse_args()


def resolve_file(raw_dir: Path, prefix: str) -> Path:
    candidates = [
        raw_dir / f"{prefix}-{DATASET_NAME}.txt",
        raw_dir / f"{prefix}.txt",
    ]
    matches = sorted(raw_dir.glob(f"{prefix}-*.txt"))
    candidates.extend(matches)
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"Could not find {prefix} file in {raw_dir}")


def parse_int_list(line: str) -> list[int]:
    line = line.strip()
    if not line:
        return []
    separator = "," if "," in line else None
    return [int(part) for part in line.split(separator) if part.strip()]


def read_hyperedges(path: Path) -> list[tuple[int, ...]]:
    with path.open("r", encoding="utf-8") as file:
        return [tuple(parse_int_list(line)) for line in file if line.strip()]


def read_label_names(path: Path) -> dict[int, str]:
    with path.open("r", encoding="utf-8") as file:
        return {index + 1: line.strip() for index, line in enumerate(file) if line.strip()}


def read_node_metadata(path: Path, label_names: dict[int, str]) -> dict[int, dict[str, list[str]]]:
    metadata = {}
    with path.open("r", encoding="utf-8") as file:
        for node_id, line in enumerate(file, start=1):
            label_ids = parse_int_list(line)
            labels = [label_names[label_id] for label_id in label_ids if label_id in label_names]
            if labels:
                metadata[node_id] = {"label": labels}
    return metadata


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    hyperedges = read_hyperedges(resolve_file(raw_dir, "hyperedges"))
    label_names = read_label_names(resolve_file(raw_dir, "label-names"))
    node_metadata = read_node_metadata(resolve_file(raw_dir, "node-labels"), label_names)

    hypergraph = Hypergraph(weighted=False)
    nodes_added = set()
    for edge in hyperedges:
        for node in edge:
            if node in nodes_added:
                continue
            nodes_added.add(node)
            hypergraph.add_node(node, metadata=node_metadata.get(node))
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
