# contacts-science-gallery reproducibility

## Dataset
- Name: contacts-science-gallery
- Description: Temporal face-to-face proximity contacts. Nodes represent individuals. Original data are pairwise contacts; hyperedges are constructed by promoting cliques of contacts into higher-order group interactions.

## Source data
- http://www.sociopatterns.org/datasets/infectious-exhibition-dynamic-contact-networks/

## Script
- `load_science_contacts.ipynb`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   Open and run `load_science_contacts.ipynb` with the HypergraphX development environment.
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- contacts-science-gallery.json.gz
- contacts-science-gallery.hgx.gz
