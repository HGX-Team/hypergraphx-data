# coauth-cs-FOCS reproducibility

## Dataset
- Name: coauth-cs-FOCS
- Description: This dataset is a subset of the Microsoft Academic Graph in which nodes represent authors and hyperedges correspond to their publications in FOCS (a top-tier computer science conference). Papers with more than 25 authors were omitted. Note that this dataset is derived from cat-edge-MAG-10; consequently, some publications may be missing when the same set of authors published at multiple conferences in that source. In such cases, the most frequent venue of a given hyperedge was used as the interaction category, and ties were discarded.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-MAG-10/

## Script
- `generate_coauth-cs-FOCS.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/coauth-cs-FOCS/generate_coauth-cs-FOCS.py /path/to/cat-edge-MAG-10 --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `coauth-cs-FOCS.json`
- `coauth-cs-FOCS.hgx`
