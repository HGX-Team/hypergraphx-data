# contacts-hospital reproducibility

## Dataset
- Name: contacts-hospital

## Source data
- Raw directory: directory containing the required files listed below.
- Required files: hospital.dat

## Script
- `generate_contacts-hospital.py`

## Method
Build maximal cliques of pairwise contacts at each timestamp; attach hospital role metadata from the raw contact rows.

## Steps
1. Provide the raw files listed above.
2. Run:
   ```bash
   python reproducibility/contacts-hospital/generate_contacts-hospital.py /path/to/DatasetHigherOrder --output-dir data/contacts-hospital
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## Output
- `contacts-hospital.json`
- `contacts-hospital.hgx`
