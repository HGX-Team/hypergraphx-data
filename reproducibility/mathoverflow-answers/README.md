# mathoverflow-answers reproducibility

## Dataset
- Name: mathoverflow-answers
- Description: A hypergraph with hyperedges as sets of questions answered by users on MathOverflow. Nodes are labeled by the tags used in the questions. Nodes often have multiple labels.

## Source data
- https://www.cs.cornell.edu/~arb/data/mathoverflow-answers/

## Script
- `generate_mathoverflow-answers.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/mathoverflow-answers/generate_mathoverflow-answers.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `mathoverflow-answers.json`
- `mathoverflow-answers.hgx`
