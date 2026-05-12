# contacts-primary-school reproducibility

## Dataset
- Name: contacts-primary-school

## Source data
- Raw directory: directory containing the required files listed below.
- Required files: primaryschool.csv and metadata_ps.txt

## Script
- `generate_contacts-primary-school.py`

## Method
Build maximal cliques of pairwise contacts at each timestamp; attach class/sex metadata from metadata_ps.txt.

## Steps
1. Provide the raw files listed above.
2. Run:
   ```bash
   python reproducibility/contacts-primary-school/generate_contacts-primary-school.py /path/to/DatasetHigherOrder --output-dir data/contacts-primary-school
   ```
3. Validate the printed node/edge counts and generated file sizes.

## Output
- `contacts-primary-school.json`
- `contacts-primary-school.hgx`
