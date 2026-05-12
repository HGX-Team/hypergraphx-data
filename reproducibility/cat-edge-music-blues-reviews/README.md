# cat-edge-music-blues-reviews reproducibility

## Dataset
- Name: cat-edge-music-blues-reviews
- Description: Hypergraph where nodes are Amazon reviewers and hyperedges are reviewers who reviewed a certain product category (different types of blues music) within a month timeframe.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-music-blues-reviews/

## Script
- `generate_cat-edge-music-blues-reviews.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cat-edge-music-blues-reviews/generate_cat-edge-music-blues-reviews.py /path/to/cat-edge-music-blues-reviews --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-music-blues-reviews.json`
- `cat-edge-music-blues-reviews.hgx`
