# cat-edge-Cooking reproducibility

## Dataset
- Name: cat-edge-Cooking
- Description: Hypergraph where nodes are food ingredients, hyperedges are recipes made from combining multiple ingredients and categories indicate cuisine (e.g., Southern-US, Indian, Spanish).

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-Cooking/

## Script
- `generate_cat-edge-Cooking.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cat-edge-Cooking/generate_cat-edge-Cooking.py /path/to/cat-edge-Cooking --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-Cooking.json`
- `cat-edge-Cooking.hgx`
