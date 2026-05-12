# NDC-classes reproducibility

## Dataset
- Name: NDC-classes
- Description: Nodes represent drug class labels. Each hyperedge represents a drug and contains the set of class labels applied to that drug. This is a temporal higher-order network dataset from the National Drug Code (NDC) Directory, maintained by the U.S. Food and Drug Administration under the Drug Listing Act of 1972. Timestamps are in days and represent when the drug was first marketed.

## Source data
- https://www.cs.cornell.edu/~arb/data/NDC-classes/

## Script
- `generate_NDC-classes.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/NDC-classes/generate_NDC-classes.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `NDC-classes.json`
- `NDC-classes.hgx`
