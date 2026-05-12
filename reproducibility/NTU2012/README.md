# NTU2012 reproducibility

## Dataset
- Name: NTU2012
- Description: National Taiwan University 3D model dataset from Chen et al (Chen et al. 2003] Chen, D.-Y.; Tian, X.-P.; Shen, Y.-T.; and Ouhyoung, M. 2003. On Visual Similarity Based 3D Model Retrieval. In Computer Graph). The NTU dataset is composed of 2,012 3D shapes from 67 categories, including car, chair, chess, chip, clock, cup, door, frame, pen, plant leaf and so on. The graph structure is constructed using a probability graph based on node distance. See 'Hypergraph Neural Networks' (https://arxiv.org/pdf/1809.09401) for details on construction.

## Source data
- https://github.com/jianhao2016/AllSet?tab=readme-ov-file

## Script
- `generate_NTU2012.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/NTU2012/generate_NTU2012.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `NTU2012.json`
- `NTU2012.hgx`
