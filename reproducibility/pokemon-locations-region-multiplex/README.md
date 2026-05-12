# pokemon-locations-region-multiplex reproducibility

## Dataset
- Name: pokemon-locations-region-multiplex
- Description: Multiplex Pokémon encounter hypergraph. Nodes represent Pokémon, layers represent regions, and each hyperedge contains the Pokémon encounterable in a location area in that region.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-locations-region-multiplex.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files:
   ```bash
   python scripts/maintenance/get_pokemon_csvs.py --output-dir /path/to/pokemon-data
   ```
2. Run:
   ```bash
   python reproducibility/pokemon-locations-region-multiplex/generate_pokemon-locations-region-multiplex.py /path/to/pokemon-data --output-dir data/pokemon-locations-region-multiplex
   ```
3. Validate the printed node/edge counts and generated file sizes.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-locations-region-multiplex.json`
- `pokemon-locations-region-multiplex.hgx`
