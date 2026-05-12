# Mushroom reproducibility

## Dataset
- Name: Mushroom
- Description: The Mushroom dataset includes descriptions of hypothetical samples corresponding to 23 species of gilled mushrooms in the Agaricus and Lepiota Family. Each node corresponds to an instance of a mushroom and hyperedges are constructed according to co-occurrences of specific attribute values. For example, all mushrooms with a brown cap form a hyperedge. There are 8124 instances (nodes) described by 22 categorical attributes, leading to a total of 272 hyperedges. Construction following the methodology used by the authors of 'YOU ARE ALLSET: A MULTISET LEARNING FRAME-WORK FOR HYPERGRAPH NEURAL NETWORKS'.

## Source data
- https://github.com/jianhao2016/AllSet?tab=readme-ov-file

## Script
- `generate_Mushroom.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/Mushroom/generate_Mushroom.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `Mushroom.json`
- `Mushroom.hgx`
