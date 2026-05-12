#!/usr/bin/env python3
"""Generate contacts-high-school-multiplex from the catalog high-school JSON."""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
from typing import Any

from hypergraphx import MultiplexHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "contacts-high-school-multiplex"
SOURCE_FILE = "contacts-high-school.json"
COMPRESSED_SOURCE_FILE = f"{SOURCE_FILE}.gz"
DAY_LAYERS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
CONTACT_INTERVAL_SECONDS = 20


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "raw_dir",
        type=Path,
        help=f"Directory containing {SOURCE_FILE} or {COMPRESSED_SOURCE_FILE}.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def source_path(raw_dir: Path) -> Path:
    if raw_dir.is_file():
        return raw_dir
    for filename in (COMPRESSED_SOURCE_FILE, SOURCE_FILE):
        path = raw_dir / filename
        if path.exists():
            return path
    raise FileNotFoundError(f"Expected {SOURCE_FILE} or {COMPRESSED_SOURCE_FILE} in {raw_dir}")


def read_source(raw_dir: Path) -> Any:
    path = source_path(raw_dir)
    open_func = gzip.open if path.suffix == ".gz" else open
    with open_func(path, "rt", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def read_catalog_json(raw_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    data = read_source(raw_dir)
    if not isinstance(data, list):
        raise ValueError("Expected the catalog contacts-high-school JSON list format")

    nodes = []
    hyperedges = []
    for item in data:
        if item.get("type") == "node":
            nodes.append({"id": item["idx"], **(item.get("metadata") or {})})
        elif item.get("type") == "edge":
            metadata = item.get("metadata") or {}
            hyperedges.append(
                {
                    "interaction": item["interaction"],
                    "time": metadata.get("original_time", metadata.get("time")),
                }
            )

    return nodes, hyperedges


def day_layers(hyperedges: list[dict[str, Any]]) -> dict[int, str]:
    last_time = -1
    day_index = 0
    layer_by_position: dict[int, str] = {}

    for index, edge in enumerate(hyperedges):
        timestamp = int(edge["time"])
        if last_time == -1 or timestamp - last_time <= CONTACT_INTERVAL_SECONDS:
            last_time = timestamp
        else:
            day_index += 1
            if day_index >= len(DAY_LAYERS):
                raise ValueError("More contact-day layers than expected")
            last_time = timestamp
        layer_by_position[index] = DAY_LAYERS[day_index]

    return layer_by_position


def build_hypergraph(raw_dir: Path) -> MultiplexHypergraph:
    nodes, hyperedges = read_catalog_json(raw_dir)
    hypergraph = MultiplexHypergraph(weighted=False)

    for node in nodes:
        node_metadata = dict(node)
        node_id = int(node_metadata["id"])
        hypergraph.add_node(node_id, metadata=node_metadata)

    hyperedges = sorted(hyperedges, key=lambda edge: int(edge["time"]))
    layer_by_position = day_layers(hyperedges)

    for index, edge in enumerate(hyperedges):
        layer = layer_by_position[index]
        interaction = tuple(sorted(int(node) for node in edge["interaction"]))
        hypergraph.add_edge(interaction, layer=layer, metadata={"layer": layer})

    hypergraph.set_attr_to_hypergraph_metadata("name", DATASET_NAME)
    hypergraph.set_attr_to_hypergraph_metadata("version", "1.0.0")
    hypergraph.set_attr_to_hypergraph_metadata("node_type", "student")
    hypergraph.set_attr_to_hypergraph_metadata("edge_type", "contact_clique")
    hypergraph.set_attr_to_hypergraph_metadata("layer_type", "school_day")
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
