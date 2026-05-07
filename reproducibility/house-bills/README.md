# house-bills reproducibility

## Dataset
- Name: house-bills
- Description: Nodes represent legislators. Each hyperedge represents a bill and contains the set of legislators associated with that bill (e.g., sponsor and cosponsor lists).

## Source data
- https://www.cs.cornell.edu/~arb/data/house-bills/

## Script
- `generate_house-bills.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_house-bills.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- house-bills.json.gz
- house-bills.hgx.gz
