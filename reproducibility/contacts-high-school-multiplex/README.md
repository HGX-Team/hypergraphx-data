# contacts-high-school-multiplex reproducibility

## Dataset
- Name: contacts-high-school-multiplex
- Description: Multiplex version of the Marseilles high-school contact dataset. Nodes represent students, hyperedges represent clique-promoted face-to-face contact groups, and layers correspond to the five observed school days.

## Original source
- http://www.sociopatterns.org/datasets/high-school-contact-and-friendship-networks/

## Reproducibility input
- The script rebuilds this multiplex dataset from the existing catalog export of `contacts-high-school`: `contacts-high-school.json.gz` (or uncompressed `contacts-high-school.json`).

## Script
- `generate_contacts-high-school-multiplex.py`

## Steps
1. Download or access the existing `contacts-high-school` JSON export from this catalog.
2. Place `contacts-high-school.json.gz` (or uncompressed `contacts-high-school.json`) in a raw-data directory.
3. Run:
   ```bash
   python reproducibility/contacts-high-school-multiplex/generate_contacts-high-school-multiplex.py /path/to/raw --output-dir /path/to/output
   ```
4. The script writes both JSON and HGX files and reloads them for validation.

## Output
- contacts-high-school-multiplex.json
- contacts-high-school-multiplex.hgx
