# NDC-substances reproducibility

## Dataset
- Name: NDC-substances
- Description: Nodes represent chemical substances. Each hyperedge represents a drug (identified by its NDC code) and contains the set of substances that make up that drug. This is a temporal higher-order network dataset from the National Drug Code (NDC) Directory, maintained by the U.S. Food and Drug Administration under the Drug Listing Act of 1972.

## Source data
- https://www.cs.cornell.edu/~arb/data/NDC-substances/

## Script
- `generate_NDC-substances.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_NDC-substances.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- NDC-substances.json.gz
- NDC-substances.hgx.gz
