#!/usr/bin/env python3
"""Generate one movie-cast hypergraph for each TMDB genre."""

from __future__ import annotations

import argparse
import ast
import csv
from pathlib import Path
from typing import Any

from hypergraphx import Hypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


MOVIES_FILE = "movies_metadata.csv"
CREDITS_FILE = "credits.csv"
TMDB_GENRES = {
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "Foreign",
    "History",
    "Horror",
    "Music",
    "Mystery",
    "Romance",
    "Science Fiction",
    "TV Movie",
    "Thriller",
    "War",
    "Western",
}
DATASET_BY_GENRE = {
    "Action": "movies-cast-action",
    "Adventure": "movies-cast-adventure",
    "Animation": "movies-cast-animation",
    "Comedy": "movies-cast-comedy",
    "Crime": "movies-cast-crime",
    "Documentary": "movies-cast-documentary",
    "Drama": "movies-cast-drama",
    "Family": "movies-cast-family",
    "Fantasy": "movies-cast-fantasy",
    "Foreign": "movies-cast-foreign",
    "History": "movies-cast-history",
    "Horror": "movies-cast-horror",
    "Music": "movies-cast-music",
    "Mystery": "movies-cast-mystery",
    "Romance": "movies-cast-romance",
    "Science Fiction": "movies-cast-science-fiction",
    "TV Movie": "movies-cast-tv-movie",
    "Thriller": "movies-cast-thriller",
    "War": "movies-cast-war",
    "Western": "movies-cast-western",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "raw_dir",
        type=Path,
        help=f"Directory containing {MOVIES_FILE} and {CREDITS_FILE}.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    return parser.parse_args()


def parse_literal(value: str, default: Any) -> Any:
    if value is None or value == "":
        return default
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return default


def parse_int(value: object) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def release_year(value: str) -> int | None:
    if not value:
        return None
    return parse_int(value.split("-", 1)[0])


def read_credits(raw_dir: Path) -> tuple[dict[str, tuple[int, ...]], dict[int, dict[str, object]]]:
    cast_by_movie: dict[str, tuple[int, ...]] = {}
    actor_metadata: dict[int, dict[str, object]] = {}

    with (raw_dir / CREDITS_FILE).open(newline="", encoding="utf-8") as file_obj:
        for row in csv.DictReader(file_obj):
            movie_id = row.get("id", "")
            cast = parse_literal(row.get("cast", ""), [])
            actor_ids = []
            seen = set()
            for actor in cast:
                if not isinstance(actor, dict):
                    continue
                actor_id = parse_int(actor.get("id"))
                if actor_id is None or actor_id in seen:
                    continue
                seen.add(actor_id)
                actor_ids.append(actor_id)
                actor_metadata.setdefault(
                    actor_id,
                    {
                        "tmdb_person_id": actor_id,
                        "name": actor.get("name", ""),
                        "gender": parse_int(actor.get("gender")) or 0,
                    },
                )
            cast_by_movie[movie_id] = tuple(sorted(actor_ids))

    return cast_by_movie, actor_metadata


def genre_names(value: str) -> list[str]:
    genres = parse_literal(value, [])
    out = []
    for genre in genres:
        if not isinstance(genre, dict):
            continue
        name = genre.get("name")
        if name in TMDB_GENRES and name not in out:
            out.append(name)
    return out


def build_hypergraphs(raw_dir: Path) -> dict[str, Hypergraph]:
    cast_by_movie, actor_metadata = read_credits(raw_dir)
    hypergraphs = {genre: Hypergraph(weighted=True) for genre in DATASET_BY_GENRE}
    active_nodes = {genre: set() for genre in DATASET_BY_GENRE}
    edge_records = {genre: [] for genre in DATASET_BY_GENRE}

    with (raw_dir / MOVIES_FILE).open(newline="", encoding="utf-8") as file_obj:
        for row in csv.DictReader(file_obj):
            movie_id = row.get("id", "")
            cast = cast_by_movie.get(movie_id, ())
            if len(cast) < 2:
                continue

            genres = genre_names(row.get("genres", ""))
            if not genres:
                continue

            metadata = {
                "movie_ids": [movie_id],
                "titles": [row.get("title") or row.get("original_title") or ""],
                "original_languages": [row.get("original_language", "")],
            }
            year = release_year(row.get("release_date", ""))
            if year is not None:
                metadata["release_years"] = [year]

            for genre in genres:
                active_nodes[genre].update(cast)
                edge_records[genre].append((cast, dict(metadata)))

    for genre, hypergraph in hypergraphs.items():
        dataset_name = DATASET_BY_GENRE[genre]
        for node in sorted(active_nodes[genre]):
            hypergraph.add_node(node, metadata=actor_metadata.get(node, {"tmdb_person_id": node}))
        for cast, metadata in edge_records[genre]:
            hypergraph.add_edge(cast, weight=1, metadata=metadata)
        hypergraph.set_attr_to_hypergraph_metadata("name", dataset_name)
        hypergraph.set_attr_to_hypergraph_metadata("version", "1.0.0")
        hypergraph.set_attr_to_hypergraph_metadata("genre", genre)
        hypergraph.set_attr_to_hypergraph_metadata("node_type", "actor")
        hypergraph.set_attr_to_hypergraph_metadata("edge_type", "movie_cast")

    return hypergraphs


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    hypergraphs = build_hypergraphs(args.raw_dir)

    for genre in sorted(hypergraphs):
        dataset_name = DATASET_BY_GENRE[genre]
        dataset_dir = args.output_dir / dataset_name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        json_path = dataset_dir / f"{dataset_name}.json"
        hgx_path = dataset_dir / f"{dataset_name}.hgx"
        save_hypergraph(hypergraphs[genre], str(json_path), fmt="json")
        save_hypergraph(hypergraphs[genre], str(hgx_path), fmt="pickle")

        for path in (json_path, hgx_path):
            loaded = load_hypergraph(str(path))
            print(f"{path}: nodes={len(loaded.get_nodes())} edges={len(loaded.get_edges())}")


if __name__ == "__main__":
    main()
