# cat-edge-vegas-bars-reviews reproducibility

## Dataset
- Name: cat-edge-vegas-bars-reviews
- Description: Hypergraph where nodes are Yelp users and hyperedges are users who reviewed an establishment of a particular category (different types of bars in Las Vegas, NV) within a month timeframe.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-vegas-bars-reviews/

## Script
- `generate_cat-edge-vegas-bars-reviews.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cat-edge-vegas-bars-reviews/generate_cat-edge-vegas-bars-reviews.py /path/to/cat-edge-vegas-bars-reviews --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-vegas-bars-reviews.json`
- `cat-edge-vegas-bars-reviews.hgx`
