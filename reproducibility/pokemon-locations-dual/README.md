# pokemon-locations-dual reproducibility

## Dataset
- Name: pokemon-locations-dual
- Description: Nodes represent PokéAPI location areas and hyperedges represent Pokémon. Each hyperedge contains the set of location areas where a Pokémon can be encountered in at least one game version.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-locations-dual.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files listed in the script docstring.
2. Run:
   ```bash
   python reproducibility/pokemon-locations-dual/generate_pokemon-locations-dual.py /path/to/pokemon-data --output-dir data/pokemon-locations-dual
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-locations-dual.json`
- `pokemon-locations-dual.hgx`
