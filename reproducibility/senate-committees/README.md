# senate-committees reproducibility

## Dataset
- Name: senate-committees
- Description: Nodes represent legislators. Each hyperedge represents a committee and contains the set of legislators serving on that committee.

## Source data
- https://www.cs.cornell.edu/~arb/data/senate-committees/

## Script
- `generate_senate-committees.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/senate-committees/generate_senate-committees.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `senate-committees.json`
- `senate-committees.hgx`
