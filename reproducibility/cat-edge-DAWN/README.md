# cat-edge-DAWN reproducibility

## Dataset
- Name: cat-edge-DAWN
- Description: In this dataset, nodes are drugs and hyperedges are combinations of drugs taken by a patient prior to an emergency room visit. Hyperedge categories indicate the patient disposition (e.g., 'sent home', 'surgery', 'released to detox').

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-DAWN/

## Script
- `generate_cat-edge-DAWN.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/cat-edge-DAWN/generate_cat-edge-DAWN.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-DAWN.json`
- `cat-edge-DAWN.hgx`
