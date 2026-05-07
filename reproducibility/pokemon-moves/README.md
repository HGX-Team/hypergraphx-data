# pokemon-moves reproducibility

## Dataset
- Name: pokemon-moves
- Description: Nodes represent Pokémon and hyperedges represent moves. Each hyperedge contains the set of Pokémon that can learn a given move in at least one version group by any learn method.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-moves.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files listed in the script docstring.
2. Run:
   ```bash
   python reproducibility/pokemon-moves/generate_pokemon-moves.py /path/to/pokemon-data --output-dir data/pokemon-moves
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-moves.json`
- `pokemon-moves.hgx`
