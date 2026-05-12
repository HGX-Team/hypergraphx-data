# coauth-cs-multiplex reproducibility

## Dataset
- Name: coauth-cs-multiplex
- Description: The MAG-10 multiplex hypergraph is a subset of the Microsoft Academic Graph where nodes are authors and hyperedges represent publications by those authors. The hypergraph is organized into layers, each corresponding to one of 10 computer science conferences (e.g., “WWW”, “KDD”, “ICML”). Within each layer, hyperedges capture publications at that specific venue. If the same set of authors published together at multiple conferences, we assigned the hyperedge to the layer of their most frequent venue, discarding cases where there was a tie. Papers with more than 25 authors were also omitted.

## Source data
- https://www.cs.cornell.edu/~arb/data/cat-edge-MAG-10/

## Script
- `generate_coauth-cs-multiplex.py`

Use the raw files from the linked source and keep the upstream filenames expected by the reproduction code.

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run:
   ```bash
   python reproducibility/coauth-cs-multiplex/generate_coauth-cs-multiplex.py /path/to/cat-edge-MAG-10 --output-dir /path/to/output
   ```
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `coauth-cs-multiplex.json`
- `coauth-cs-multiplex.hgx`
