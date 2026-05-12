# cat-edge-MAG-10 reproducibility

## Dataset
- Name: cat-edge-MAG-10
- Description: The MAG-10 network is a subset of the Microsoft Academic Graph where nodes are authors, hyperedges correspond to a publication from those authors, and the hyperedges are categorized by one of 10 computer science confereneces (e.g., 'WWW', 'KDD', 'ICML'). If the same set of authors published at more than one conference, we used the most common venue as the category and any cases where there is a tie were discarded. Papers with more than 25 authors were also omitted.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-MAG-10/

## Script
- `generate_cat-edge-MAG-10.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/cat-edge-MAG-10/generate_cat-edge-MAG-10.py /path/to/cat-edge-MAG-10 --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `cat-edge-MAG-10.json`
- `cat-edge-MAG-10.hgx`
