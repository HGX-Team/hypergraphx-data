# cat-edge-algebra-questions reproducibility

## Dataset
- Name: cat-edge-algebra-questions
- Description: Hypergraph where nodes are users on MathOverflow and hyperedges are sets of users who answered a certain question category (derived from different tags involving algebra).

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-algebra-questions/

## Script
- `generate_cat-edge-algebra-questions.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cat-edge-algebra-questions/generate_cat-edge-algebra-questions.py /path/to/cat-edge-algebra-questions --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-algebra-questions.json`
- `cat-edge-algebra-questions.hgx`
