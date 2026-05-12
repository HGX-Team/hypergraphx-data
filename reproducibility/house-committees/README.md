# house-committees reproducibility

## Dataset
- Name: house-committees
- Description: Nodes represent legislators. Each hyperedge represents a committee and contains the set of legislators serving on that committee.

## Source data
- https://www.cs.cornell.edu/~arb/data/house-committees/

## Script
- `generate_house-committees.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/house-committees/generate_house-committees.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `house-committees.json`
- `house-committees.hgx`
