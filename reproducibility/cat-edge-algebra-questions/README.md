# cat-edge-algebra-questions reproducibility

## Dataset
- Name: cat-edge-algebra-questions
- Description: Hypergraph where nodes are users on MathOverflow and hyperedges are sets of users who answered a certain question category (derived from different tags involving algebra).

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-algebra-questions/

## Script
- `load_cat-edge.ipynb`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   Open and run `load_cat-edge.ipynb` with the HypergraphX development environment.
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- cat-edge-algebra-questions.json.gz
- cat-edge-algebra-questions.hgx.gz
