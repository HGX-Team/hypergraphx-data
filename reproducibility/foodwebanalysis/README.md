# foodwebanalysis reproducibility

## Dataset
- Name: foodwebanalysis
- Description: The data is collected from the Florida Bay food web. Bifan motifs in the original directed carbon-flow network are converted into submodular hyperedges. Available node labels/classes indicate whether a food-web compartment is a producer, a low-level consumer, or a high-level consumer.

## Source data
- https://sites.google.com/view/panli-purdue/datasets/foodweb?authuser=0

## Script
- `generate_foodwebanalysis.py`

## Steps
1. Download or access the source data from the link above.
2. Place `Florida-bay-meta.csv` and `foodweb-hyper.csv` in a raw-data directory.
3. Run:
   ```bash
   python reproducibility/foodwebanalysis/generate_foodwebanalysis.py /path/to/raw --output-dir /path/to/output
   ```
4. The script writes both JSON and HGX files and reloads them for validation.

## Output
- foodwebanalysis.json
- foodwebanalysis.hgx
