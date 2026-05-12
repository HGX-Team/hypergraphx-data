# cora reproducibility

## Dataset
- Name: cora
- Description: Co-citation network of scientific publications. Nodes correspond to publications. Each article is a centroid and forms a hyperedge that connects the article with all publications that cite it or are cited by it.

## Source data
- https://github.com/jianhao2016/AllSet?tab=readme-ov-file

## Script
- `generate_cora.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/cora/generate_cora.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cora.json`
- `cora.hgx`
