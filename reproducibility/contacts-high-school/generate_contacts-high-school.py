#!/usr/bin/env python3
"""Generate contacts-high-school from local Sociopatterns raw contact data."""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx

from hypergraphx import TemporalHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph

DATASET_NAME = "contacts-high-school"

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


def load_classes_and_sex(path: Path) -> dict[int, dict]:
    metadata = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            node_raw, class_id, sex = line.split()
            node = int(node_raw)
            metadata[node] = {"class": class_id, "id": node, "sex": sex}
    return metadata


def load_friendship_lists(path: Path) -> dict[int, list[int]]:
    friends = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            source_raw, target_raw = line.split()[:2]
            friends.setdefault(int(source_raw), []).append(int(target_raw))
    # The first entry for each respondent is an administrative marker in this
    # source file and is not part of the curated questionnaire-friends list.
    return {node: values[1:] for node, values in friends.items()}


def load_facebook_lists(path: Path) -> dict[int, list[int]]:
    friends = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            source_raw, target_raw, known_raw = line.split()[:3]
            if int(known_raw) == 1:
                source = int(source_raw)
                target = int(target_raw)
                friends.setdefault(source, []).append(target)
                friends.setdefault(target, []).append(source)
    return friends


def build_hypergraph(raw_dir: Path) -> TemporalHypergraph:
    contacts_by_time, node_order = load_pair_contacts(raw_dir / "High-School_data_2013.csv")
    metadata = load_classes_and_sex(raw_dir / "meta_hs.txt")
    questionnaire = load_friendship_lists(raw_dir / "Friendship-network_data_2013.csv")
    facebook = load_facebook_lists(raw_dir / "Facebook-known-pairs_data_2013.csv")

    hypergraph = TemporalHypergraph(weighted=False)
    for node in node_order:
        node_metadata = dict(metadata.get(node, {"id": node}))
        if node in facebook:
            node_metadata["has_facebook"] = True
            node_metadata["facebook_friends"] = facebook[node]
        else:
            node_metadata["has_facebook"] = False
        if node in questionnaire:
            node_metadata["has_compiled_questionnaire"] = True
            node_metadata["questionnaire_friends"] = questionnaire[node]
        else:
            node_metadata["has_compiled_questionnaire"] = False
        hypergraph.add_node(node, metadata=node_metadata)
    add_clique_edges(hypergraph, contacts_by_time)
    return hypergraph


def main() -> None:
    args = parse_args()
    hypergraph = build_hypergraph(args.raw_dir)
    save_and_validate(hypergraph, args.output_dir)


if __name__ == "__main__":
    main()
