# coauth-cs-KDD reproducibility

## Dataset
- Name: coauth-cs-KDD
- Description: This dataset is a subset of the Microsoft Academic Graph in which nodes represent authors and hyperedges correspond to their publications in KDD (a top-tier computer science conference). Papers with more than 25 authors were omitted. Note that this dataset is derived from cat-edge-MAG-10; consequently, some publications may be missing when the same set of authors published at multiple conferences in that source. In such cases, the most frequent venue of a given hyperedge was used as the interaction category, and ties were discarded.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-MAG-10/

## Script
- `load_MAG10.ipynb`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   Open and run `load_MAG10.ipynb` with the HypergraphX development environment.
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- coauth-cs-KDD.json.gz
- coauth-cs-KDD.hgx.gz
