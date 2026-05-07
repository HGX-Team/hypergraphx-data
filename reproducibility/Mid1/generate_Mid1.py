#!/usr/bin/env python3
"""Generate Mid1 from Utah school temporal contact data."""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx

from hypergraphx import TemporalHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "Mid1"
DEFAULT_RAW_DIR = Path(DATASET_NAME) / "raw"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "raw_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help=f"Directory containing tij_{DATASET_NAME}.txt.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def read_original_networks(raw_dir: Path) -> dict[int, nx.Graph]:
    path = raw_dir / f"tij_{DATASET_NAME}.txt"
    networks: dict[int, nx.Graph] = {}

    with path.open() as file_obj:
        for line in file_obj:
            if not line.strip():
                continue
            time_value, node_i, node_j = map(int, line.split())
            time_value *= 20
            networks.setdefault(time_value, nx.Graph()).add_edge(node_i, node_j)

    return networks


def build_hypergraph(raw_dir: Path) -> TemporalHypergraph:
    networks = read_original_networks(raw_dir)
    temporal_hypergraph = TemporalHypergraph()

    for time_value in sorted(networks):
        cliques = [tuple(clique) for clique in nx.find_cliques(networks[time_value])]
        temporal_hypergraph.add_edges(
            edge_list=cliques,
            time_list=[time_value] * len(cliques),
        )

    return temporal_hypergraph


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
