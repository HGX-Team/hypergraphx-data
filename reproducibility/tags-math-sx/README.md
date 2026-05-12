# tags-math-sx reproducibility

## Dataset
- Name: tags-math-sx
- Description: Nodes represent tags. Hyperedges represent questions on math.stackexchange.com and contain the set of tags applied to each question. The timestamps are recorded at millisecond resolution but are normalized to start at 0.

## Source data
- https://www.cs.cornell.edu/~arb/data/tags-math-sx/

## Script
- `generate_tags-math-sx.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/tags-math-sx/generate_tags-math-sx.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `tags-math-sx.json`
- `tags-math-sx.hgx`
