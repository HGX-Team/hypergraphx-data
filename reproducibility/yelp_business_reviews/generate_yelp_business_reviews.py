#!/usr/bin/env python3
"""Generate yelp_business_reviews from AllSet Yelp raw files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DATASET_NAME = "yelp_business_reviews"
DEFAULT_RAW_DIR = Path("AllSet_all_raw_data") / "yelp"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def build_hypergraph(raw_dir: Path) -> Hypergraph:
    latlong = pd.read_csv(raw_dir / "yelp_restaurant_latlong.csv").values
    business_stars = pd.read_csv(raw_dir / "yelp_restaurant_business_stars.csv")
    names = pd.read_csv(raw_dir / "yelp_restaurant_name.csv").values.flatten()
    incidences = pd.read_csv(raw_dir / "yelp_restaurant_incidence_H.csv")

    node_metadata = {}
    for index, name in enumerate(names):
        node_id = index + 1
        node_metadata[node_id] = {
            "lat": str(float(latlong[index, 0])),
            "long": str(float(latlong[index, 1])),
            "business_stars": int(business_stars["business_stars"].iloc[index]),
            "name": str(name),
        }

    incidences = incidences.assign(
        he=incidences["he"].astype(int),
        node=incidences["node"].astype(int),
    )
    hyperedges = (
        incidences.groupby("he")["node"]
        .agg(lambda values: sorted(set(values.tolist())))
        .to_dict()
    )

    hypergraph = Hypergraph()
    hypergraph.add_nodes(node_list=list(node_metadata), metadata=node_metadata)
    for edge_id, edge in hyperedges.items():
        hypergraph.add_edge(edge=edge, metadata={"edge_id": int(edge_id)})

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
