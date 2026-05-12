# cooking-southern_us reproducibility

## Dataset
- Name: cooking-southern_us
- Description: Recipe hypergraph from Southern US cuisine (the United States (Southern US)). Nodes represent ingredients. Each hyperedge represents a recipe and contains the set of ingredients used in that recipe.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-Cooking/

## Script
- `generate_cooking-southern_us.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cooking-southern_us/generate_cooking-southern_us.py /path/to/cat-edge-Cooking --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cooking-southern_us.json`
- `cooking-southern_us.hgx`
