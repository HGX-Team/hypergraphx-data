# pokemon-moves-version-group-multiplex reproducibility

## Dataset
- Name: pokemon-moves-version-group-multiplex
- Description: Multiplex Pokémon move hypergraph. Nodes represent Pokémon, layers represent game version groups, and each hyperedge contains Pokémon that can learn a move in that version group.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-moves-version-group-multiplex.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files listed in the script docstring.
2. Run:
   ```bash
   python reproducibility/pokemon-moves-version-group-multiplex/generate_pokemon-moves-version-group-multiplex.py /path/to/pokemon-data --output-dir data/pokemon-moves-version-group-multiplex
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-moves-version-group-multiplex.json`
- `pokemon-moves-version-group-multiplex.hgx`
