# amazon-reviews reproducibility

## Dataset
- Name: amazon-reviews
- Description: Hypergraph built from Amazon product reviews (specifically, the collection of 5-core datasets). Nodes represent products and each hyperedge represents the set of products reviewed by a user. Nodes are labeled by product category.

## Source data
- https://www.cs.cornell.edu/~arb/data/amazon-reviews/

## Script
- `generate_amazon-reviews.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/amazon-reviews/generate_amazon-reviews.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `amazon-reviews.json`
- `amazon-reviews.hgx`
