# senate-committees reproducibility

## Dataset
- Name: senate-committees
- Description: Nodes represent legislators. Each hyperedge represents a committee and contains the set of legislators serving on that committee.

## Source data
- https://www.cs.cornell.edu/~arb/data/senate-committees/

## Script
- `generate_senate-committees.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_senate-committees.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- senate-committees.json.gz
- senate-committees.hgx.gz
