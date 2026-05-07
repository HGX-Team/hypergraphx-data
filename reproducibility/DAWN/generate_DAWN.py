#!/usr/bin/env python3
"""Generate the standalone DAWN dataset from the ARB/Cornell archive."""

from __future__ import annotations

import argparse
import tarfile
import tempfile
from collections import Counter
from pathlib import Path

from hypergraphx import TemporalHypergraph
from hypergraphx.readwrite import load_hypergraph, save_hypergraph


DEFAULT_ARCHIVE_URL = "https://drive.google.com/uc?export=download&id=1wGwoG7oBWnNN7J9TEpjqNpODbsYfMxp4"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "archive",
        type=Path,
        help="Path to DAWN.tar.gz downloaded from the ARB dataset page.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/DAWN"),
        help="Directory where DAWN.json and DAWN.hgx will be written.",
    )
    return parser.parse_args()


def read_ints(path: Path) -> list[int]:
    with path.open("r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file if line.strip()]


def read_node_metadata(path: Path) -> dict[int, dict[str, str]]:
    metadata = {}
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(maxsplit=2)
            if len(parts) == 3:
                node_id, drug_code, drug_name = parts
                metadata[int(node_id)] = {
                    "drug_code": drug_code,
                    "drug_name": drug_name,
                }
            elif len(parts) == 2:
                node_id, drug_name = parts
                metadata[int(node_id)] = {"drug_name": drug_name}
    return metadata


def timestamp_to_year_quarter(timestamp: int) -> tuple[int, int]:
    """Cornell encodes quarter-year timestamps as year * 4 + quarter."""
    return (timestamp - 1) // 4, ((timestamp - 1) % 4) + 1


def build_hypergraph(raw_dir: Path) -> TemporalHypergraph:
    nverts = read_ints(raw_dir / "DAWN-nverts.txt")
    simplices = read_ints(raw_dir / "DAWN-simplices.txt")
    times = read_ints(raw_dir / "DAWN-times.txt")
    node_metadata = read_node_metadata(raw_dir / "DAWN-node-labels.txt")

    if len(nverts) != len(times):
        raise ValueError("DAWN-nverts.txt and DAWN-times.txt have different lengths")
    if sum(nverts) != len(simplices):
        raise ValueError("DAWN-simplices.txt length does not match sum(DAWN-nverts.txt)")

    min_time = min(times)
    offset = 0
    edge_counts: Counter[tuple[int, tuple[int, ...]]] = Counter()
    for size, timestamp in zip(nverts, times):
        edge = tuple(sorted(simplices[offset : offset + size]))
        offset += size
        edge_counts[(timestamp, edge)] += 1

    hypergraph = TemporalHypergraph(weighted=True)
    for node, metadata in node_metadata.items():
        hypergraph.add_node(node, metadata=metadata)

    for (timestamp, edge), weight in edge_counts.items():
        year, quarter = timestamp_to_year_quarter(timestamp)
        hypergraph.add_edge(
            edge,
            timestamp - min_time,
            weight=weight,
            metadata={
                "original_timestamp": timestamp,
                "year": year,
                "quarter": quarter,
            },
        )

    return hypergraph


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        with tarfile.open(args.archive, "r:gz") as archive:
            archive.extractall(temp_dir)

        hypergraph = build_hypergraph(temp_dir / "DAWN")
        hypergraph.set_attr_to_hypergraph_metadata("name", "DAWN")
        hypergraph.set_attr_to_hypergraph_metadata("version", "1.0.0")

        json_path = output_dir / "DAWN.json"
        hgx_path = output_dir / "DAWN.hgx"
        save_hypergraph(hypergraph, str(json_path), fmt="json")
        save_hypergraph(hypergraph, str(hgx_path), fmt="pickle")

    # Fail fast if a generated artifact cannot be read by HypergraphX.
    for path in (json_path, hgx_path):
        loaded = load_hypergraph(str(path))
        print(
            f"{path}: nodes={len(loaded.get_nodes())} "
            f"temporal_edges={len(loaded.get_edges())}"
        )


if __name__ == "__main__":
    main()
