#!/usr/bin/env python3
"""Generate contacts-science-gallery from raw contact-list files."""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx

from hypergraphx import TemporalHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "contacts-science-gallery"
DEFAULT_RAW_DIR = Path("sg_infectious_contact_list")
TIME_SHIFT = 1240913019


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path, help="Directory containing the raw Sociopatterns files.")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def build_hypergraph(raw_dir: Path) -> TemporalHypergraph:
    nodes = set()
    temporal_edges = []

    for path in sorted(raw_dir.iterdir()):
        if not path.is_file():
            continue
        date = path.name[13:-4].replace("_", "-")
        contacts_by_time = {}
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                timestamp_raw, source_raw, target_raw = line.split()
                timestamp = int(timestamp_raw)
                source = int(source_raw)
                target = int(target_raw)
                contacts_by_time.setdefault(timestamp, []).append((source, target))
                nodes.add(source)
                nodes.add(target)

        for timestamp, contacts in contacts_by_time.items():
            graph = nx.Graph(contacts)
            for clique in nx.find_cliques(graph):
                temporal_edges.append({"interaction": tuple(sorted(clique)), "time": timestamp, "date": date})

    hypergraph = TemporalHypergraph()
    for node in nodes:
        hypergraph.add_node(node)
    for edge in temporal_edges:
        hypergraph.add_edge(
            edge["interaction"],
            time=edge["time"] - TIME_SHIFT,
            metadata={"date": edge["date"], "original_time": edge["time"]},
        )

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
