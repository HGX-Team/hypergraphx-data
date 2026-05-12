# trivago-clicks reproducibility

## Dataset
- Name: trivago-clicks
- Description: A hypergraph where nodes are accommodations (mostly hotels), and hyperedges are sets of accommodations for which a user performed the 'click-out' action during the same browsing session.

## Source data
- https://www.cs.cornell.edu/~arb/data/trivago-clicks/

## Script
- `generate_trivago-clicks.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/trivago-clicks/generate_trivago-clicks.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `trivago-clicks.json`
- `trivago-clicks.hgx`
