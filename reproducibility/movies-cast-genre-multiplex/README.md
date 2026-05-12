# movies-cast-genre-multiplex reproducibility

## Dataset
- Name: movies-cast-genre-multiplex
- Description: Multiplex movie-cast hypergraph built from The Movies Dataset. Nodes are actors, hyperedges are movie casts, and layers are movie genres. Movies with multiple genres are added to every corresponding genre layer.

## Source data
- https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

## Construction
- Nodes are TMDB actor/person identifiers from `credits.csv`.
- Each hyperedge is the cast of one movie, restricted to movies with at least 2 distinct actors.
- Layers are the 20 standard TMDB movie genres present in `movies_metadata.csv`.
- Movies with multiple genres are inserted in every corresponding genre layer.
- Repeated normalized casts in the same genre layer are collapsed into one weighted hyperedge.

## Script
- `generate_movies-cast-genre-multiplex.py`

## Steps
1. Download The Movies Dataset from the link above.
2. Place `movies_metadata.csv` and `credits.csv` in a raw-data directory.
3. Run:
   ```bash
   python reproducibility/movies-cast-genre-multiplex/generate_movies-cast-genre-multiplex.py /path/to/raw --output-dir /path/to/output
   ```
4. The script writes both JSON and HGX files and reloads them for validation.

## Output
- movies-cast-genre-multiplex.json
- movies-cast-genre-multiplex.hgx

Expected output statistics:
- nodes: 202689
- hyperedges: 86918
- layers: 20
- maximum hyperedge size: 312
