# pokemon-encounter-method-multiplex reproducibility

## Dataset
- Name: pokemon-encounter-method-multiplex
- Description: Multiplex Pokémon encounter hypergraph. Nodes represent Pokémon, layers represent encounter methods, and each hyperedge contains Pokémon encounterable in a location area by that method.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-encounter-method-multiplex.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files listed in the script docstring.
2. Run:
   ```bash
   python reproducibility/pokemon-encounter-method-multiplex/generate_pokemon-encounter-method-multiplex.py /path/to/pokemon-data --output-dir data/pokemon-encounter-method-multiplex
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-encounter-method-multiplex.json`
- `pokemon-encounter-method-multiplex.hgx`
