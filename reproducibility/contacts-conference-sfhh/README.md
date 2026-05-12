# contacts-conference-sfhh reproducibility

## Dataset
- Name: contacts-conference-sfhh

## Source data
- Raw directory: directory containing the required files listed below.
- Required files: conference.dat

## Script
- `generate_contacts-conference-sfhh.py`

## Method
Build maximal cliques of pairwise contacts at each timestamp; attach attendee id metadata.

## Steps
1. Provide the raw files listed above.
2. Run:
   ```bash
   python reproducibility/contacts-conference-sfhh/generate_contacts-conference-sfhh.py /path/to/DatasetHigherOrder --output-dir data/contacts-conference-sfhh
   ```
3. Validate the printed node/edge counts and generated file sizes.

## Output
- `contacts-conference-sfhh.json`
- `contacts-conference-sfhh.hgx`
