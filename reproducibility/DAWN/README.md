# DAWN reproducibility

## Dataset
- Name: DAWN
- Description: The Drug Abuse Warning Network (DAWN) temporal higher-order network. Nodes are drugs and each timestamped hyperedge is the set of drugs reported by a patient during an emergency department visit. Timestamps are encoded at quarter-year resolution from 2004 to 2011.

## Source data
- https://www.cs.cornell.edu/~arb/data/DAWN/

The source archive is `DAWN.tar.gz`, linked from the ARB dataset page.

## Script
- `generate_DAWN.py`

## Steps
1. Download `DAWN.tar.gz` from the source page.
2. Run:
   ```bash
   python reproducibility/DAWN/generate_DAWN.py /path/to/DAWN.tar.gz --output-dir data/DAWN
   ```
3. Validate the printed node/edge counts and generated file sizes.

## Output
- `DAWN.json`
- `DAWN.hgx`
