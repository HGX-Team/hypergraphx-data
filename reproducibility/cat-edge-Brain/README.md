# cat-edge-Brain reproducibility

## Dataset
- Name: cat-edge-Brain
- Description: Nodes represent brain regions from an MRI scan. Hyperedges (pairs) represent connections between regions and are labeled with one of two categories: high fMRI correlation or similar activation patterns.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-Brain/

## Script
- `generate_cat-edge-Brain.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cat-edge-Brain/generate_cat-edge-Brain.py /path/to/cat-edge-Brain --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-Brain.json`
- `cat-edge-Brain.hgx`
