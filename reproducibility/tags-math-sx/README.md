# tags-math-sx reproducibility

## Dataset
- Name: tags-math-sx
- Description: Nodes represent tags. Hyperedges represent questions on math.stackexchange.com and contain the set of tags applied to each question. The timestamps are recorded at millisecond resolution but are normalized to start at 0.

## Source data
- https://www.cs.cornell.edu/~arb/data/tags-math-sx/

## Script
- `generate_tags-math-sx.py`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   python generate_tags-math-sx.py
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- tags-math-sx.json.gz
- tags-math-sx.hgx.gz
