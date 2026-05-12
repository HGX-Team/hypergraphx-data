# movies-cast-by-genre reproducibility

## Dataset collection
This folder reproduces the single-genre movie-cast hypergraphs derived from The Movies Dataset. Nodes are actors, hyperedges are movie casts, and each generated dataset contains only movies from one TMDB genre.

## Source data
- https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
- Required files: `movies_metadata.csv` and `credits.csv`
- The Kaggle dataset page lists the license as CC0: Public Domain. The movie details and credits were collected from the TMDB Open API; this derived collection uses TMDB data but is not endorsed or certified by TMDB.

## Construction
- Nodes are TMDB actor/person identifiers from `credits.csv`.
- Each hyperedge is the cast of one movie, restricted to movies with at least 2 distinct actors.
- The collection uses the 20 standard TMDB movie genres present in `movies_metadata.csv`.
- Movies with multiple genres are included in every corresponding single-genre dataset.
- Repeated normalized casts within the same genre are collapsed into one weighted hyperedge.

## Script
- `generate_movies-cast-by-genre.py`

## Steps
1. Download The Movies Dataset from the link above.
2. Place `movies_metadata.csv` and `credits.csv` in a raw-data directory.
3. Run:
   ```bash
   python reproducibility/movies-cast-by-genre/generate_movies-cast-by-genre.py /path/to/raw --output-dir /path/to/output
   ```
4. The script writes JSON and HGX files for each genre and reloads them for validation.

## Output datasets
- movies-cast-action
- movies-cast-adventure
- movies-cast-animation
- movies-cast-comedy
- movies-cast-crime
- movies-cast-documentary
- movies-cast-drama
- movies-cast-family
- movies-cast-fantasy
- movies-cast-foreign
- movies-cast-history
- movies-cast-horror
- movies-cast-music
- movies-cast-mystery
- movies-cast-romance
- movies-cast-science-fiction
- movies-cast-thriller
- movies-cast-tv-movie
- movies-cast-war
- movies-cast-western
