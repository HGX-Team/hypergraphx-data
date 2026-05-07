# pokemon-moves-learn-method-full-multiplex reproducibility

## Dataset
- Name: pokemon-moves-learn-method-full-multiplex
- Description: Multiplex Pokémon move hypergraph. Nodes represent Pokémon, layers represent move learn methods, and each hyperedge contains Pokémon that can learn a move by that method, including all learn methods present in PokéAPI.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-moves-learn-method-full-multiplex.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files listed in the script docstring.
2. Run:
   ```bash
   python reproducibility/pokemon-moves-learn-method-full-multiplex/generate_pokemon-moves-learn-method-full-multiplex.py /path/to/pokemon-data --output-dir data/pokemon-moves-learn-method-full-multiplex
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-moves-learn-method-full-multiplex.json`
- `pokemon-moves-learn-method-full-multiplex.hgx`
