# coauth-geology reproducibility

## Dataset
- Name: coauth-geology
- Description: Nodes represent authors. Each hyperedge represents a publication and contains the set of co-authors of that publication. This is a temporal higher-order network dataset, where each hyperedge is a publication marked with the Geology tag in the Microsoft Academic Graph. Timestamps are the year of publication.

## Source data
- https://www.cs.cornell.edu/~arb/data/coauth-MAG-Geology/

## Script
- `generate_coauth-geology.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/coauth-geology/generate_coauth-geology.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `coauth-geology.json`
- `coauth-geology.hgx`
