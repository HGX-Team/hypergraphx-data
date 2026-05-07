# zoo reproducibility

## Dataset
- Name: zoo
- Description: Nodes correspond to animals in the Zoo database and use integer ids. Hyperedges correspond to shared attributes, i.e., each hyperedge contains the set of animals that share a given attribute. Node metadata records the animal name and type class.

## Source data
- https://archive.ics.uci.edu/dataset/111/zoo

## Script
- `generate_zoo.py`

## Steps
1. Download or access the source data from the link above.
2. Place `zoo.data` in a raw-data directory.
3. Run:
   ```bash
   python reproducibility/zoo/generate_zoo.py /path/to/raw --output-dir /path/to/output
   ```
4. The script writes both JSON and HGX files and reloads them for validation.

## Output
- zoo.json
- zoo.hgx
