# cat-edge-music-blues-reviews reproducibility

## Dataset
- Name: cat-edge-music-blues-reviews
- Description: Hypergraph where nodes are Amazon reviewers and hyperedges are reviewers who reviewed a certain product category (different types of blues music) within a month timeframe.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-music-blues-reviews/

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
- cat-edge-music-blues-reviews.json.gz
- cat-edge-music-blues-reviews.hgx.gz
