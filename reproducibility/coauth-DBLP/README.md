# coauth-DBLP reproducibility

## Dataset
- Name: coauth-DBLP
- Description: Nodes represent authors. Each hyperedge represents a publication and contains the set of co-authors of that publication. This is a temporal higher-order network dataset, where each hyperedge is a publication recorded on DBLP. Timestamps are the year of publication.

## Source data
- https://www.cs.cornell.edu/~arb/data/coauth-DBLP/

## Script
- `generate_coauth-DBLP.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_coauth-DBLP.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- coauth-DBLP.json.gz
- coauth-DBLP.hgx.gz
