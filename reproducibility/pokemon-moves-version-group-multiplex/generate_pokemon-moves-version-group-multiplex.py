#!/usr/bin/env python3
"""Generate pokemon-moves-version-group-multiplex from local PokéAPI-derived CSV files.

The expected raw files are the CSVs produced by the PokéAPI extraction script:
pokemon.csv, moves.csv, location_areas.csv, pokemon_move_raw.csv,
pokemon_location_raw.csv, incidence_moves_any.csv, and incidence_locations_any.csv.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd
from hypergraphx import Hypergraph, MultiplexHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph

DATASET_NAME = 'pokemon-moves-version-group-multiplex'
CORE_METHODS = {"level-up", "machine", "egg", "tutor"}

SINGLETON_EDGE_FIELDS = {
    "pokemon-encounter-method-multiplex": {"encounter_methods"},
    "pokemon-locations-region-multiplex": {"regions"},
    "pokemon-locations-version-multiplex": {"versions", "n_observations"},
    "pokemon-moves-dual": {"min_level"},
    "pokemon-moves-learn-method-full-multiplex": {"learn_methods"},
    "pokemon-moves-learn-method-multiplex": {"learn_methods"},
    "pokemon-moves-version-group-multiplex": {"version_groups"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path, help="Directory containing the PokéAPI-derived CSV files.")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def clean(value):
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        value = value.item()
    return value


def clean_dict(data: dict) -> dict:
    out = {}
    for key, value in data.items():
        value = clean(value)
        if value not in (None, ""):
            out[key] = value
    return out


def sorted_unique(values):
    out = []
    seen = set()
    for value in values:
        value = clean(value)
        if value in (None, "") or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return sorted(out)


def aggregate_meta(existing: dict, extra: dict) -> dict:
    for key, value in extra.items():
        if value in (None, ""):
            continue
        values = value if isinstance(value, list) else [value]
        bucket = existing.setdefault(key, [])
        for item in values:
            if item not in bucket:
                bucket.append(item)
    return existing


def finalize_meta(metadata: dict) -> dict:
    out = {}
    singleton_fields = SINGLETON_EDGE_FIELDS.get(DATASET_NAME, set())
    for key, value in metadata.items():
        if isinstance(value, list):
            if key in singleton_fields and len(value) == 1:
                out[key] = value[0]
                continue
            try:
                out[key] = sorted(value)
            except TypeError:
                out[key] = value
        else:
            out[key] = value
    return out


def pokemon_metadata(pokemon: pd.DataFrame) -> dict[int, dict]:
    meta = {}
    for row in pokemon.itertuples(index=False):
        meta[int(row.pokemon_id)] = clean_dict({
            "pokemon_id": row.pokemon_id,
            "name": row.pokemon_name,
            "species": row.species_name,
            "generation": row.generation_name,
            "is_default": bool(row.is_default),
            "primary_type": row.primary_type,
            "secondary_type": row.secondary_type,
            "height": row.height,
            "weight": row.weight,
            "base_hp": row.base_hp,
            "base_attack": row.base_attack,
            "base_defense": row.base_defense,
            "base_sp_attack": row.base_sp_attack,
            "base_sp_defense": row.base_sp_defense,
            "base_speed": row.base_speed,
        })
    return meta


def move_metadata(moves: pd.DataFrame) -> dict[int, dict]:
    meta = {}
    for row in moves.itertuples(index=False):
        meta[int(row.move_id)] = clean_dict({
            "move_id": row.move_id,
            "name": row.move_name,
            "type": row.move_type,
            "damage_class": row.damage_class,
            "power": row.power,
            "accuracy": row.accuracy,
            "pp": row.pp,
            "generation": row.generation_name,
        })
    return meta


def location_metadata(locations: pd.DataFrame) -> dict[int, dict]:
    meta = {}
    for row in locations.itertuples(index=False):
        meta[int(row.location_area_id)] = clean_dict({
            "location_area_id": row.location_area_id,
            "area_name": row.location_area_name,
            "location_name": row.location_name,
            "region": row.region_name,
        })
    return meta


def add_nodes(hypergraph, node_metadata: dict) -> None:
    for node, metadata in node_metadata.items():
        hypergraph.add_node(node, metadata=metadata)


def build_hypergraph(node_metadata: dict, edge_map: dict, metadata: dict) -> Hypergraph:
    hypergraph = Hypergraph(weighted=False)
    add_nodes(hypergraph, node_metadata)
    for edge, edge_metadata in sorted(edge_map.items(), key=lambda item: (len(item[0]), item[0])):
        if edge:
            hypergraph.add_edge(edge, metadata=finalize_meta(edge_metadata))
    for key, value in metadata.items():
        hypergraph.set_attr_to_hypergraph_metadata(key, value)
    return hypergraph


def build_multiplex(node_metadata: dict, edge_map: dict, metadata: dict) -> MultiplexHypergraph:
    hypergraph = MultiplexHypergraph(weighted=False)
    add_nodes(hypergraph, node_metadata)
    for (layer, edge), edge_metadata in sorted(edge_map.items(), key=lambda item: (str(item[0][0]), len(item[0][1]), item[0][1])):
        if edge:
            hypergraph.add_edge(edge, layer=layer, metadata=finalize_meta(edge_metadata))
    for key, value in metadata.items():
        hypergraph.set_attr_to_hypergraph_metadata(key, value)
    return hypergraph


def save_dataset(name: str, hypergraph, output_dir: Path) -> None:
    dataset_dir = output_dir
    dataset_dir.mkdir(parents=True, exist_ok=True)
    json_path = dataset_dir / f"{name}.json"
    hgx_path = dataset_dir / f"{name}.hgx"
    save_hypergraph(hypergraph, str(json_path), fmt="json")
    save_hypergraph(hypergraph, str(hgx_path), fmt="pickle")
    json_loaded = load_hypergraph(str(json_path), fmt="json")
    hgx_loaded = load_hypergraph(str(hgx_path), fmt="pickle")
    if len(json_loaded.get_edges()) != len(hypergraph.get_edges()) or len(hgx_loaded.get_nodes()) != len(hypergraph.get_nodes()):
        raise RuntimeError(f"Roundtrip mismatch for {name}")
    if isinstance(hypergraph, MultiplexHypergraph):
        json_loaded.get_edges(metadata=True)
        hgx_loaded.get_edges(metadata=True)


def load_tables(raw_dir: Path):
    pokemon = pd.read_csv(raw_dir / "pokemon.csv")
    moves = pd.read_csv(raw_dir / "moves.csv")
    locations = pd.read_csv(raw_dir / "location_areas.csv")
    pokemon_moves = pd.read_csv(raw_dir / "pokemon_move_raw.csv")
    pokemon_locations = pd.read_csv(raw_dir / "pokemon_location_raw.csv")
    incidence_moves = pd.read_csv(raw_dir / "incidence_moves_any.csv")
    incidence_locations = pd.read_csv(raw_dir / "incidence_locations_any.csv")
    return pokemon, moves, locations, pokemon_moves, pokemon_locations, incidence_moves, incidence_locations


def builders(raw_dir: Path):
    pokemon, moves, locations, pmr, plr, incm, incl = load_tables(raw_dir)
    pmeta = pokemon_metadata(pokemon)
    mmeta = move_metadata(moves)
    lmeta = location_metadata(locations)
    pmr_move = pmr.groupby("move_id")
    pmr_pokemon = pmr.groupby("pokemon_id")
    plr_location = plr.groupby("location_area_id")
    plr_pokemon = plr.groupby("pokemon_id")
    location_region = locations.set_index("location_area_id")["region_name"].to_dict()

    def move_extra(move_id: int, rows=None):
        rows = pmr_move.get_group(move_id) if rows is None and move_id in pmr_move.groups else rows
        base = mmeta.get(int(move_id), {})
        levels = [int(v) for v in rows["level"].dropna().unique() if int(v) > 0] if rows is not None else []
        return {
            "move_ids": [int(move_id)],
            "move_names": [base.get("name")],
            "move_types": [base.get("type")],
            "damage_classes": [base.get("damage_class")],
            "generations": [base.get("generation")],
            "version_groups": sorted_unique(rows["version_group"]) if rows is not None else [],
            "learn_methods": sorted_unique(rows["learn_method"]) if rows is not None else [],
            "min_level": min(levels) if levels else None,
            "n_observations": int(len(rows)) if rows is not None else 0,
        }

    def location_extra(location_id: int, rows=None):
        rows = plr_location.get_group(location_id) if rows is None and location_id in plr_location.groups else rows
        base = lmeta.get(int(location_id), {})
        return {
            "location_area_ids": [int(location_id)],
            "area_names": [base.get("area_name")],
            "location_names": [base.get("location_name")],
            "regions": [base.get("region")],
            "versions": sorted_unique(rows["version"]) if rows is not None else [],
            "encounter_methods": sorted_unique(rows["encounter_method"]) if rows is not None else [],
            "n_observations": int(len(rows)) if rows is not None else 0,
        }

    def pokemon_extra(pokemon_id: int, rows, relation: str):
        base = dict(pmeta.get(int(pokemon_id), {}))
        if relation == "moves":
            levels = [int(v) for v in rows["level"].dropna().unique() if int(v) > 0]
            base.update({"version_groups": sorted_unique(rows["version_group"]), "learn_methods": sorted_unique(rows["learn_method"]), "min_level": min(levels) if levels else None})
        else:
            base.update({"versions": sorted_unique(rows["version"]), "encounter_methods": sorted_unique(rows["encounter_method"])})
        return base

    def meta(name, node_type, edge_type, layer_type=None):
        data = {"name": name, "version": "1.0.0", "node_type": node_type, "edge_type": edge_type}
        if layer_type:
            data["layer_type"] = layer_type
        return data

    def pokemon_locations():
        edge_map = defaultdict(dict)
        for location_id, group in incl.groupby("location_area_id"):
            edge = tuple(sorted(int(x) for x in group["pokemon_id"].unique()))
            aggregate_meta(edge_map[edge], location_extra(int(location_id)))
        return build_hypergraph(pmeta, edge_map, meta("pokemon-locations", "pokemon", "location_area"))

    def pokemon_locations_dual():
        edge_map = defaultdict(dict)
        for pokemon_id, group in incl.groupby("pokemon_id"):
            edge = tuple(sorted(int(x) for x in group["location_area_id"].unique()))
            rows = plr_pokemon.get_group(pokemon_id) if pokemon_id in plr_pokemon.groups else pd.DataFrame()
            aggregate_meta(edge_map[edge], pokemon_extra(int(pokemon_id), rows, "locations"))
        return build_hypergraph(lmeta, edge_map, meta("pokemon-locations-dual", "location_area", "pokemon"))

    def pokemon_locations_version_multiplex():
        edge_map = defaultdict(dict)
        for (version, location_id), group in plr.groupby(["version", "location_area_id"]):
            edge = tuple(sorted(int(x) for x in group["pokemon_id"].unique()))
            md = location_extra(int(location_id), group)
            md["layer"] = version
            md["versions"] = [version]
            aggregate_meta(edge_map[(version, edge)], md)
        return build_multiplex(pmeta, edge_map, meta("pokemon-locations-version-multiplex", "pokemon", "location_area", "version"))

    def pokemon_locations_region_multiplex():
        edge_map = defaultdict(dict)
        for location_id, group in incl.groupby("location_area_id"):
            layer = location_region.get(int(location_id))
            if not layer or pd.isna(layer):
                continue
            edge = tuple(sorted(int(x) for x in group["pokemon_id"].unique()))
            md = location_extra(int(location_id))
            md["layer"] = layer
            md["regions"] = [layer]
            aggregate_meta(edge_map[(layer, edge)], md)
        return build_multiplex(pmeta, edge_map, meta("pokemon-locations-region-multiplex", "pokemon", "location_area", "region"))

    def pokemon_encounter_method_multiplex():
        edge_map = defaultdict(dict)
        for (method, location_id), group in plr.groupby(["encounter_method", "location_area_id"]):
            if not method or pd.isna(method):
                continue
            edge = tuple(sorted(int(x) for x in group["pokemon_id"].unique()))
            md = location_extra(int(location_id), group)
            md["layer"] = method
            md["encounter_methods"] = [method]
            aggregate_meta(edge_map[(method, edge)], md)
        return build_multiplex(pmeta, edge_map, meta("pokemon-encounter-method-multiplex", "pokemon", "location_area", "encounter_method"))

    def pokemon_moves():
        edge_map = defaultdict(dict)
        for move_id, group in incm.groupby("move_id"):
            edge = tuple(sorted(int(x) for x in group["pokemon_id"].unique()))
            aggregate_meta(edge_map[edge], move_extra(int(move_id)))
        return build_hypergraph(pmeta, edge_map, meta("pokemon-moves", "pokemon", "move"))

    def pokemon_moves_dual():
        edge_map = defaultdict(dict)
        for pokemon_id, group in incm.groupby("pokemon_id"):
            edge = tuple(sorted(int(x) for x in group["move_id"].unique()))
            rows = pmr_pokemon.get_group(pokemon_id) if pokemon_id in pmr_pokemon.groups else pd.DataFrame()
            aggregate_meta(edge_map[edge], pokemon_extra(int(pokemon_id), rows, "moves"))
        return build_hypergraph(mmeta, edge_map, meta("pokemon-moves-dual", "move", "pokemon"))

    def moves_by_learn_method(name: str, methods: set[str] | None):
        rows = pmr if methods is None else pmr[pmr["learn_method"].isin(methods)]
        edge_map = defaultdict(dict)
        for (method, move_id), group in rows.groupby(["learn_method", "move_id"]):
            edge = tuple(sorted(int(x) for x in group["pokemon_id"].unique()))
            md = move_extra(int(move_id), group)
            md["layer"] = method
            md["learn_methods"] = [method]
            aggregate_meta(edge_map[(method, edge)], md)
        return build_multiplex(pmeta, edge_map, meta(name, "pokemon", "move", "learn_method"))

    def pokemon_moves_version_group_multiplex():
        edge_map = defaultdict(dict)
        for (version_group, move_id), group in pmr.groupby(["version_group", "move_id"]):
            edge = tuple(sorted(int(x) for x in group["pokemon_id"].unique()))
            md = move_extra(int(move_id), group)
            md["layer"] = version_group
            md["version_groups"] = [version_group]
            aggregate_meta(edge_map[(version_group, edge)], md)
        return build_multiplex(pmeta, edge_map, meta("pokemon-moves-version-group-multiplex", "pokemon", "move", "version_group"))

    return {
        "pokemon-locations": pokemon_locations,
        "pokemon-locations-version-multiplex": pokemon_locations_version_multiplex,
        "pokemon-locations-region-multiplex": pokemon_locations_region_multiplex,
        "pokemon-locations-dual": pokemon_locations_dual,
        "pokemon-encounter-method-multiplex": pokemon_encounter_method_multiplex,
        "pokemon-moves": pokemon_moves,
        "pokemon-moves-dual": pokemon_moves_dual,
        "pokemon-moves-learn-method-multiplex": lambda: moves_by_learn_method("pokemon-moves-learn-method-multiplex", CORE_METHODS),
        "pokemon-moves-learn-method-full-multiplex": lambda: moves_by_learn_method("pokemon-moves-learn-method-full-multiplex", None),
        "pokemon-moves-version-group-multiplex": pokemon_moves_version_group_multiplex,
    }



def main() -> None:
    args = parse_args()
    available = builders(args.raw_dir)
    hypergraph = available[DATASET_NAME]()
    save_dataset(DATASET_NAME, hypergraph, args.output_dir)
    print(f"{DATASET_NAME}: nodes={len(hypergraph.get_nodes())} edges={len(hypergraph.get_edges())}")


if __name__ == "__main__":
    main()
