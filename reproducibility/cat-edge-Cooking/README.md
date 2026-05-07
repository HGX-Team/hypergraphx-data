# cat-edge-Cooking reproducibility

## Dataset
- Name: cat-edge-Cooking
- Description: Hypergraph where nodes are food ingredients, hyperedges are recipes made from combining multiple ingredients and categories indicate cuisine (e.g., Southern-US, Indian, Spanish).

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-Cooking/

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
- cat-edge-Cooking.json.gz
- cat-edge-Cooking.hgx.gz
