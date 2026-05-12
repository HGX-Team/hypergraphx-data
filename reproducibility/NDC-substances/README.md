# NDC-substances reproducibility

## Dataset
- Name: NDC-substances
- Description: Nodes represent chemical substances. Each hyperedge represents a drug (identified by its NDC code) and contains the set of substances that make up that drug. This is a temporal higher-order network dataset from the National Drug Code (NDC) Directory, maintained by the U.S. Food and Drug Administration under the Drug Listing Act of 1972.

## Source data
- https://www.cs.cornell.edu/~arb/data/NDC-substances/

## Script
- `generate_NDC-substances.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/NDC-substances/generate_NDC-substances.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `NDC-substances.json`
- `NDC-substances.hgx`
