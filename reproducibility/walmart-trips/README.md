# walmart-trips reproducibility

## Dataset
- Name: walmart-trips
- Description: Hypergraph of Walmart shopping trips. Nodes represent products and each hyperedge represents a trip (basket) containing the set of co-purchased products, as released as part of a Kaggle competition. Products are assigned to one of ten broad departments on walmart.com (e.g., 'Clothing, Shoes, and Accessories'), which serve as node labels (with an additional 'Other' class).

## Source data
- https://www.cs.cornell.edu/~arb/data/walmart-trips/

## Script
- `generate_walmart-trips.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/walmart-trips/generate_walmart-trips.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `walmart-trips.json`
- `walmart-trips.hgx`
