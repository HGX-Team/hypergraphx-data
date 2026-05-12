# coauth-DBLP reproducibility

## Dataset
- Name: coauth-DBLP
- Description: Nodes represent authors. Each hyperedge represents a publication and contains the set of co-authors of that publication. This is a temporal higher-order network dataset, where each hyperedge is a publication recorded on DBLP. Timestamps are the year of publication.

## Source data
- https://www.cs.cornell.edu/~arb/data/coauth-DBLP/

## Script
- `generate_coauth-DBLP.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/coauth-DBLP/generate_coauth-DBLP.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `coauth-DBLP.json`
- `coauth-DBLP.hgx`
