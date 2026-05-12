# contacts-workplace reproducibility

## Dataset
- Name: contacts-workplace

## Source data
- Raw directory: directory containing the required files listed below.
- Required files: workspace.dat

## Script
- `generate_contacts-workplace.py`

## Method
Build maximal cliques of pairwise contacts at each timestamp; attach department metadata matching the curated dataset.

## Steps
1. Provide the raw files listed above.
2. Run:
   ```bash
   python reproducibility/contacts-workplace/generate_contacts-workplace.py /path/to/DatasetHigherOrder --output-dir data/contacts-workplace
   ```
3. Validate the printed node/edge counts and generated file sizes.

## Output
- `contacts-workplace.json`
- `contacts-workplace.hgx`
