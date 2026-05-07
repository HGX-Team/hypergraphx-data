# congress-bills reproducibility

## Dataset
- Name: congress-bills
- Description: Nodes represent legislators. Each hyperedge represents a bill and contains the set of legislators associated with that bill (e.g., sponsor and cosponsor lists).

## Source data
- https://www.cs.cornell.edu/~arb/data/congress-bills/

## Script
- `generate_congress-bills.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_congress-bills.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- congress-bills.json.gz
- congress-bills.hgx.gz
