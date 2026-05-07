# pokemon-locations reproducibility

## Dataset
- Name: pokemon-locations
- Description: Nodes represent Pokémon and hyperedges represent PokéAPI location areas. Each hyperedge contains the set of Pokémon encounterable in a given location area in at least one game version or encounter method.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-locations.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files listed in the script docstring.
2. Run:
   ```bash
   python reproducibility/pokemon-locations/generate_pokemon-locations.py /path/to/pokemon-data --output-dir data/pokemon-locations
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-locations.json`
- `pokemon-locations.hgx`
