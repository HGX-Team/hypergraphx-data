# ModelNet40 reproducibility

## Dataset
- Name: ModelNet40
- Description: The Princeton ModelNet40 dataset is a benchmark dataset from the area of computer graphics first introduced by Wu et al. (Zhirong Wu, Shuran Song, Aditya Khosla, Fisher Yu, Linguang Zhang, Xiaoou Tang, and Jianxiong Xiao. 3d shapenets: A deep representation for volumetric shapes. In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 1912–1920, 2015.) The ModelNet40 dataset consists of 12,311 objects from 40 popular categories and the graph structure is constructed using a probability graph based on node distance. See 'Hypergraph Neural Networks' (https://arxiv.org/pdf/1809.09401) for details on construction.

## Source data
- https://github.com/jianhao2016/AllSet?tab=readme-ov-file

## Script
- `generate_ModelNet40.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/ModelNet40/generate_ModelNet40.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `ModelNet40.json`
- `ModelNet40.hgx`
