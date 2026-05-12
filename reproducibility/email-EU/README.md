# email-EU reproducibility

## Dataset
- Name: email-EU
- Description: Nodes represent email addresses. Each hyperedge represents an email exchange involving the set of participating addresses (and may include a timestamp/weight when available).

## Source data
- https://www.cs.cornell.edu/~arb/data/email-Eu/

## Script
- `generate_email-EU.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/email-EU/generate_email-EU.py /path/to/raw --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `email-EU.json`
- `email-EU.hgx`
