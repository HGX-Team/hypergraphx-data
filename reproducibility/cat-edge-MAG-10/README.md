# cat-edge-MAG-10 reproducibility

## Dataset
- Name: cat-edge-MAG-10
- Description: The MAG-10 network is a subset of the Microsoft Academic Graph where nodes are authors, hyperedges correspond to a publication from those authors, and the hyperedges are categorized by one of 10 computer science confereneces (e.g., 'WWW', 'KDD', 'ICML'). If the same set of authors published at more than one conference, we used the most common venue as the category and any cases where there is a tie were discarded. Papers with more than 25 authors were also omitted.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-MAG-10/

## Script
- `load_cat-edge.ipynb`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   Open and run `load_cat-edge.ipynb` with the HypergraphX development environment.
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- cat-edge-MAG-10.json.gz
- cat-edge-MAG-10.hgx.gz
