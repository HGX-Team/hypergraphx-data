# pokemon-moves-dual reproducibility

## Dataset
- Name: pokemon-moves-dual
- Description: Nodes represent moves and hyperedges represent Pokémon. Each hyperedge contains the set of moves learnable by a Pokémon in at least one version group by any learn method.

## Source data
- PokéAPI: https://pokeapi.co/
- PokéAPI static data repository: https://github.com/PokeAPI/api-data

## Script
- `generate_pokemon-moves-dual.py`

## Steps
1. Generate or provide the PokéAPI-derived CSV files listed in the script docstring.
2. Run:
   ```bash
   python reproducibility/pokemon-moves-dual/generate_pokemon-moves-dual.py /path/to/pokemon-data --output-dir data/pokemon-moves-dual
   ```
3. Validate that the generated JSON and HGX files load with HypergraphX.

## License
- License: BSD-3-Clause
- License URL: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md
- Note: Pokémon and Pokémon character names are trademarks of Nintendo. PokéAPI is not affiliated with Nintendo, Game Freak, or Creatures.

## Output
- `pokemon-moves-dual.json`
- `pokemon-moves-dual.hgx`
