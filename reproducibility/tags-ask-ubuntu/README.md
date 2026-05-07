# tags-ask-ubuntu reproducibility

## Dataset
- Name: tags-ask-ubuntu
- Description: Nodes represent tags. Hyperedges represent questions on askubuntu.com and contain the set of tags applied to each question. The timestamps are recorded at millisecond resolution but are normalized to start at 0.

## Source data
- https://www.cs.cornell.edu/~arb/data/tags-ask-ubuntu/

## Script
- `generate_tags-ask-ubuntu.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_tags-ask-ubuntu.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- tags-ask-ubuntu.json.gz
- tags-ask-ubuntu.hgx.gz
