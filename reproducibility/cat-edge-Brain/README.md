# cat-edge-Brain reproducibility

## Dataset
- Name: cat-edge-Brain
- Description: Nodes represent brain regions from an MRI scan. Hyperedges (pairs) represent connections between regions and are labeled with one of two categories: high fMRI correlation or similar activation patterns.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-Brain/

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
- cat-edge-Brain.json.gz
- cat-edge-Brain.hgx.gz
