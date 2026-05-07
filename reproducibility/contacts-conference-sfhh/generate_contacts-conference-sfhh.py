#!/usr/bin/env python3
"""Generate contacts-conference-sfhh from local Sociopatterns raw contact data."""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx

from hypergraphx import TemporalHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph

DATASET_NAME = "contacts-conference-sfhh"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path, help="Directory containing the raw Sociopatterns files.")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def ordered_unique(values):
    out = []
    seen = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def load_pair_contacts(path: Path):
    contacts_by_time = {}
    node_order = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            parts = line.split()
            timestamp = int(parts[0])
            source = int(parts[1])
            target = int(parts[2])
            contacts_by_time.setdefault(timestamp, []).append((source, target))
            node_order.extend((source, target))
    return contacts_by_time, ordered_unique(node_order)


def add_clique_edges(hypergraph: TemporalHypergraph, contacts_by_time: dict[int, list[tuple[int, int]]]) -> None:
    time_shift = min(contacts_by_time)
    for timestamp in sorted(contacts_by_time):
        graph = nx.Graph()
        graph.add_edges_from(contacts_by_time[timestamp])
        for clique in nx.find_cliques(graph):
            edge = tuple(sorted(clique))
            hypergraph.add_edge(edge, time=timestamp - time_shift, metadata={"original_time": timestamp})


def save_and_validate(hypergraph: TemporalHypergraph, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{DATASET_NAME}.json"
    hgx_path = output_dir / f"{DATASET_NAME}.hgx"
    save_hypergraph(hypergraph, str(json_path), fmt="json")
    save_hypergraph(hypergraph, str(hgx_path), fmt="pickle")
    for path in (json_path, hgx_path):
        loaded = load_hypergraph(str(path))
        print(f"{path}: nodes={len(loaded.get_nodes())} edges={len(loaded.get_edges())}")


def build_hypergraph(raw_dir: Path) -> TemporalHypergraph:
    contacts_by_time, node_order = load_pair_contacts(raw_dir / "conference.dat")
    hypergraph = TemporalHypergraph(weighted=False)
    for node in sorted(node_order):
        hypergraph.add_node(node, metadata={"id": node})
    add_clique_edges(hypergraph, contacts_by_time)
    return hypergraph


def main() -> None:
    args = parse_args()
    hypergraph = build_hypergraph(args.raw_dir)
    save_and_validate(hypergraph, args.output_dir)


if __name__ == "__main__":
    main()
