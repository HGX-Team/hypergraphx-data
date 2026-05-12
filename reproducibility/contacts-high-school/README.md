# contacts-high-school reproducibility

## Dataset
- Name: contacts-high-school

## Source data
- Raw directory: directory containing the required files listed below.
- Required files: High-School_data_2013.csv, meta_hs.txt, Friendship-network_data_2013.csv, Facebook-known-pairs_data_2013.csv

## Script
- `generate_contacts-high-school.py`

## Method
Build maximal cliques of pairwise contacts at each timestamp; attach class/sex, questionnaire friendship, and Facebook friendship metadata.

## Steps
1. Provide the raw files listed above.
2. Run:
   ```bash
   python reproducibility/contacts-high-school/generate_contacts-high-school.py /path/to/DatasetHigherOrder --output-dir data/contacts-high-school
   ```
3. Validate the printed node/edge counts and generated file sizes.

## Output
- `contacts-high-school.json`
- `contacts-high-school.hgx`
