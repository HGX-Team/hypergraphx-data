# congress-bills reproducibility

## Dataset
- Name: congress-bills
- Description: Nodes represent legislators. Each hyperedge represents a bill and contains the set of legislators associated with that bill (e.g., sponsor and cosponsor lists).

## Source data
- https://www.cs.cornell.edu/~arb/data/congress-bills/

## Script
- `generate_congress-bills.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/congress-bills/generate_congress-bills.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `congress-bills.json`
- `congress-bills.hgx`
