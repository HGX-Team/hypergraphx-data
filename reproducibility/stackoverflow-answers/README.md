# stackoverflow-answers reproducibility

## Dataset
- Name: stackoverflow-answers
- Description: A hypergraph where hyperedges are sets of questions answered by users on the website Stack Overflow. Nodes are questions, and are labeled by the tags used in the relevant question. As such, multiple labels can be assigned to a node.

## Source data
- https://www.cs.cornell.edu/~arb/data/stackoverflow-answers/

## Script
- `generate_stackoverflow-answers.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/stackoverflow-answers/generate_stackoverflow-answers.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `stackoverflow-answers.json`
- `stackoverflow-answers.hgx`
