# NDC-classes reproducibility

## Dataset
- Name: NDC-classes
- Description: Nodes represent drug class labels. Each hyperedge represents a drug and contains the set of class labels applied to that drug. This is a temporal higher-order network dataset from the National Drug Code (NDC) Directory, maintained by the U.S. Food and Drug Administration under the Drug Listing Act of 1972. Timestamps are in days and represent when the drug was first marketed.

## Source data
- https://www.cs.cornell.edu/~arb/data/NDC-classes/

## Script
- `generate_NDC-classes.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_NDC-classes.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- NDC-classes.json.gz
- NDC-classes.hgx.gz
