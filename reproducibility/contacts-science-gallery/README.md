# contacts-science-gallery reproducibility

## Dataset
- Name: contacts-science-gallery
- Description: Temporal face-to-face proximity contacts. Nodes represent individuals. Original data are pairwise contacts; hyperedges are constructed by promoting cliques of contacts into higher-order group interactions.

## Source data
- http://www.sociopatterns.org/datasets/infectious-exhibition-dynamic-contact-networks/

## Script
- `generate_contacts-science-gallery.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/contacts-science-gallery/generate_contacts-science-gallery.py /path/to/sg_infectious_contact_list --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `contacts-science-gallery.json`
- `contacts-science-gallery.hgx`
