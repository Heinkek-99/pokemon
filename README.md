# Pokedex

Petit projet en deux parties : une API qui interroge la PokeAPI publique, et une interface de
consultation.

## Contenu

- `api.py` : API Flask. Expose la liste des Pokémon, la fiche d'un Pokémon par son nom et les
  types disponibles. Les données viennent de https://pokeapi.co
- `ui.py` : interface Streamlit. Recherche par nom, filtre par type, tableau des résultats et
  graphiques avec matplotlib.

## Lancer le projet

API, port 5000 par défaut :

```bash
pip install flask requests
python api.py
```

Interface, dans un second terminal :

```bash
pip install streamlit requests pandas matplotlib
streamlit run ui.py
```

L'interface lit `http://localhost:5000/api/`.

## État

Projet d'exercice terminé et fonctionnel. Il m'a servi à pratiquer Flask et Streamlit, dont je me
sers ensuite dans des projets d'analyse de données.
