# cooking-thai reproducibility

## Dataset
- Name: cooking-thai
- Description: Recipe hypergraph from Thai cuisine (Thailand). Nodes represent ingredients. Each hyperedge represents a recipe and contains the set of ingredients used in that recipe.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-Cooking/

## Script
- `generate_cooking-thai.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cooking-thai/generate_cooking-thai.py /path/to/cat-edge-Cooking --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cooking-thai.json`
- `cooking-thai.hgx`
