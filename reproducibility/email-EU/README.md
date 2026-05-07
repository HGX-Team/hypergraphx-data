# email-EU reproducibility

## Dataset
- Name: email-EU
- Description: Nodes represent email addresses. Each hyperedge represents an email exchange involving the set of participating addresses (and may include a timestamp/weight when available).

## Source data
- https://www.cs.cornell.edu/~arb/data/email-Eu/

## Script
- `generate_email-EU.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_email-EU.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- email-EU.json.gz
- email-EU.hgx.gz
