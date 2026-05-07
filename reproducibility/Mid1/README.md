# Mid1 reproducibility

## Dataset
- Name: Mid1
- Description: A temporal network describing face-to-face interactions of students in a middle school in Utah, USA. Nodes represent individuals. Original data are pairwise contacts; hyperedges are constructed by promoting cliques of contacts into higher-order group interactions.

## Source data
- https://royalsocietypublishing.org/doi/suppl/10.1098/rsif.2015.0279

## Script
- `generate_Mid1.py`

## Steps
1. Download or access the source data from the link above.
2. Place `tij_Mid1.txt` in a raw-data directory.
3. Run:
   ```bash
   python reproducibility/Mid1/generate_Mid1.py /path/to/raw --output-dir /path/to/output
   ```
4. The script writes both JSON and HGX files and reloads them for validation.

## Output
- Mid1.json
- Mid1.hgx
