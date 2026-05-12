# cat-edge-madison-restaurant-reviews reproducibility

## Dataset
- Name: cat-edge-madison-restaurant-reviews
- Description: Hypergraph where nodes are Yelp users and hyperedges are users who reviewed an establishment of a particular category (different types of restaurants in Madison, WI) within a month timeframe.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-madison-restaurant-reviews/

## Script
- `generate_cat-edge-madison-restaurant-reviews.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cat-edge-madison-restaurant-reviews/generate_cat-edge-madison-restaurant-reviews.py /path/to/cat-edge-madison-restaurant-reviews --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-madison-restaurant-reviews.json`
- `cat-edge-madison-restaurant-reviews.hgx`
