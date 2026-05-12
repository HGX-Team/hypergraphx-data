# 20newsW100 reproducibility

## Dataset
- Name: 20newsW100
- Description: Nodes represent news articles. Each hyperedge represents a word and contains the set of articles in which that word occurs. A dataset from the UCI Categorical Machine Learning Repository. The dataset contains 16,242 articles with binary occurrence values of 100 words. Each word is regarded as a hyperedge and the news articles are vertices. Dataset construction following Yang et al. (Chaoqi Yang, Ruijie Wang, Shuochao Yao, and Tarek Abdelzaher. Hypergraph learning with line expansion. arXiv preprint arXiv:2005.04843, 2020.).

## Source data
- https://github.com/jianhao2016/AllSet?tab=readme-ov-file

## Script
- `generate_20newsW100.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/20newsW100/generate_20newsW100.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `20newsW100.json`
- `20newsW100.hgx`
