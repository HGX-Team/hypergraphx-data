# tags-stack-overflow reproducibility

## Dataset
- Name: tags-stack-overflow
- Description: Nodes represent tags. Hyperedges represent questions on stackoverflow.com and contain the set of tags applied to each question. The timestamps are recorded at millisecond resolution but are normalized to start at 0.

## Source data
- https://www.cs.cornell.edu/~arb/data/tags-stack-overflow/

## Script
- `generate_tags-stack-overflow.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/tags-stack-overflow/generate_tags-stack-overflow.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `tags-stack-overflow.json`
- `tags-stack-overflow.hgx`
