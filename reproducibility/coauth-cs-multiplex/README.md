# coauth-cs-multiplex reproducibility

## Dataset
- Name: coauth-cs-multiplex
- Description: The MAG-10 multiplex hypergraph is a subset of the Microsoft Academic Graph where nodes are authors and hyperedges represent publications by those authors. The hypergraph is organized into layers, each corresponding to one of 10 computer science conferences (e.g., “WWW”, “KDD”, “ICML”). Within each layer, hyperedges capture publications at that specific venue. If the same set of authors published together at multiple conferences, we assigned the hyperedge to the layer of their most frequent venue, discarding cases where there was a tie. Papers with more than 25 authors were also omitted.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-MAG-10/

## Script
- `load_MAG10.ipynb`

The script expects the source data directory names used by the original conversion workflow; adjust paths if running from another location.

## Steps
1. Download or access the source data from the link above.
2. Place the source data in the directory expected by the script.
3. Run:
   ```bash
   Open and run `load_MAG10.ipynb` with the HypergraphX development environment.
   ```
4. Validate that the generated JSON and HGX files load with HypergraphX, then gzip them for publication.

## Output
- coauth-cs-multiplex.json.gz
- coauth-cs-multiplex.hgx.gz
