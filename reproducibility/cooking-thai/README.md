# cooking-thai reproducibility

## Dataset
- Name: cooking-thai
- Description: Recipe hypergraph from Thai cuisine (Thailand). Nodes represent ingredients. Each hyperedge represents a recipe and contains the set of ingredients used in that recipe.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-Cooking/

## Script
- `load_cooking.ipynb`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   Open and run `load_cooking.ipynb` with the HypergraphX development environment.
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- cooking-thai.json.gz
- cooking-thai.hgx.gz
