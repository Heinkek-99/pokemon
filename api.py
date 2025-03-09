from flask import Flask, jsonify
import requests

app = Flask(__name__)
url = "https://pokeapi.co/api/v2/"

# Helper pour les requêtes API
def fetch_pokeapi(endpoint):
    response = requests.get(f"{url}/{endpoint}")
    return response.json() if response.status_code == 200 else None

@app.route('/api/pokemon', methods=['GET'])
def get_all_pokemon():
    data = fetch_pokeapi("pokemon?limit=1000")
    return jsonify([pokemon['name'] for pokemon in data['results']])

@app.route('/api/pokemon/<name>', methods=['GET'])
def get_pokemon(name):
    data = fetch_pokeapi(f"pokemon/{name.lower()}")
    if not data:
        return jsonify({"error": "Pokémon non trouvé"}), 404
    
    return jsonify({
        "name": data['name'],
        "height": data['height'],
        "weight": data['weight'],
        "types": [t['type']['name'] for t in data['types']],
        "image": data['sprites']['front_default']
    })

@app.route('/api/pokemon/type/<type_name>', methods=['GET'])
def get_pokemon_by_type(type_name):
    data = fetch_pokeapi(f"type/{type_name.lower()}")
    if not data:
        return jsonify({"error": "Type non trouvé"}), 404
    
    pokemon_list = [p['pokemon']['name'] for p in data['pokemon']]
    return jsonify(pokemon_list)

@app.route('/api/types', methods=['GET'])
def get_all_types():
    try:
        data = fetch_pokeapi("type?limit=20")
        if not data:
            return jsonify({"error": "Échec de récupération des types"}), 500
            
        types = [t['name'] for t in data['results'] if t['name'] not in ['unknown', 'shadow']]
        return jsonify(types)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)