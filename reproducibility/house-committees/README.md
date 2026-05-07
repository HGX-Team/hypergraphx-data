# house-committees reproducibility

## Dataset
- Name: house-committees
- Description: Nodes represent legislators. Each hyperedge represents a committee and contains the set of legislators serving on that committee.

## Source data
- https://www.cs.cornell.edu/~arb/data/house-committees/

## Script
- `generate_house-committees.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_house-committees.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- house-committees.json.gz
- house-committees.hgx.gz
