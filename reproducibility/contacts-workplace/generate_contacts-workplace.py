#!/usr/bin/env python3
"""Generate contacts-workplace from local Sociopatterns raw contact data."""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx

from hypergraphx import TemporalHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph

DATASET_NAME = "contacts-workplace"

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


DEPARTMENTS = {
    35: 'DISQ',
    184: 'DISQ',
    751: 'DISQ',
    255: 'DISQ',
    131: 'DISQ',
    273: 'DISQ',
    743: 'DISQ',
    210: 'DISQ',
    826: 'DISQ',
    265: 'DISQ',
    845: 'DISQ',
    185: 'DISQ',
    268: 'DISQ',
    778: 'DISQ',
    253: 'DISQ',
    172: 'DSE',
    513: 'DSE',
    29: 'DSE',
    272: 'DSE',
    79: 'DSE',
    181: 'DSE',
    196: 'DSE',
    56: 'DSE',
    164: 'DSE',
    242: 'DSE',
    223: 'DSE',
    120: 'DSE',
    311: 'DSE',
    496: 'DSE',
    132: 'DSE',
    819: 'DSE',
    603: 'DSE',
    267: 'DSE',
    222: 'DSE',
    205: 'DSE',
    662: 'DSE',
    113: 'DSE',
    123: 'DSE',
    39: 'DSE',
    779: 'DSE',
    95: 'DSE',
    791: 'DSE',
    194: 'DSE',
    786: 'DSE',
    15: 'DSE',
    494: 'DSE',
    765: 'DSE',
    987: 'DSE',
    939: 'DSE',
    87: 'SFLE',
    213: 'SFLE',
    211: 'SFLE',
    116: 'SFLE',
    209: 'DMCT',
    938: 'DMCT',
    875: 'DMCT',
    179: 'DMCT',
    80: 'DMCT',
    21: 'DMCT',
    101: 'DMCT',
    48: 'DMCT',
    511: 'DMCT',
    102: 'DMCT',
    762: 'DMCT',
    66: 'DMCT',
    134: 'DMCT',
    17: 'DMCT',
    119: 'DMCT',
    771: 'DMCT',
    784: 'DMCT',
    105: 'DMCT',
    118: 'DMCT',
    431: 'DMCT',
    285: 'DMCT',
    240: 'DMCT',
    804: 'DMCT',
    335: 'DMCT',
    50: 'DMCT',
    275: 'DMCT',
    709: 'SRH',
    533: 'SRH',
    448: 'SRH',
    481: 'SRH',
    154: 'SRH',
    122: 'SRH',
    492: 'SRH',
    153: 'SRH',
    601: 'SRH',
    271: 'SRH',
    63: 'SRH',
    150: 'SRH',
    499: 'SRH',
}


def build_hypergraph(raw_dir: Path) -> TemporalHypergraph:
    contacts_by_time, _ = load_pair_contacts(raw_dir / "workspace.dat")
    hypergraph = TemporalHypergraph(weighted=False)
    for node, department in DEPARTMENTS.items():
        hypergraph.add_node(node, metadata={"id": node, "department": department})
    add_clique_edges(hypergraph, contacts_by_time)
    return hypergraph


def main() -> None:
    args = parse_args()
    hypergraph = build_hypergraph(args.raw_dir)
    save_and_validate(hypergraph, args.output_dir)


if __name__ == "__main__":
    main()
