import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_BASE_URL = "http://localhost:5000/api/"

# Configuration de la page
st.set_page_config(page_title="Pokedex", layout="wide")
st.title("📗 Pokedex Interactif")

# Sidebar pour les filtres
with st.sidebar:
    st.header("Filtres")
    search_name = st.text_input("Rechercher par nom")
    selected_type = st.selectbox("Filtrer par type", requests.get(f"{API_BASE_URL}/types").json())

try:
    type_response = requests.get(f"{API_BASE_URL}/types")
    type_response.raise_for_status()
    all_types = ['Tous'] + type_response.json()  # Ajout d'une option par défaut
except Exception as e:
    st.error(f"Erreur API : {str(e)}")
    all_types = ['Tous']

selected_type = st.selectbox(
    "Filtrer par type",
    all_types,
    index=0
)

# Section principale
col1, col2 = st.columns([1, 2])

with col1:
    if search_name:
        try :
            response = requests.get(f"{API_BASE_URL}/pokemon/{search_name}", timeout=10)

            response.raise_for_status()
            
            pokemon_data = response.json()
    
            st.success(f"Pokémon trouvé : {pokemon_data['name'].title()}")
            col_img, col_stats = st.columns([1, 2])
                
            with col_img:
                st.image(
                    pokemon_data['image'],
                    caption=pokemon_data['name'].title(),
                    width=200
                )
            
            with col_stats:
                st.metric("🏔️ Taille", f"{pokemon_data['height']/10} m")
                st.metric("⚖️ Poids", f"{pokemon_data['weight']/10} kg")
                st.markdown(f"**🎨 Types:** {' | '.join(t.upper() for t in pokemon_data['types'])}")
                    
        except requests.exceptions.HTTPError:
            st.error("Pokémon introuvable")
        except Exception as e:
            st.error(f"Erreur : {str(e)}")

            
            if 'error' not in pokemon_data:
                st.subheader(pokemon_data['name'].capitalize())
                st.image(pokemon_data['image'], width=200)
                st.metric("Taille", f"{pokemon_data['height']/10} m")
                st.metric("Poids", f"{pokemon_data['weight']/10} kg")
                st.write("**Types:**", ", ".join(pokemon_data['types']).title())

    elif selected_type:
        pokemons = requests.get(f"{API_BASE_URL}/pokemon/type/{selected_type}").json()
        st.subheader(f"Pokémons de type {selected_type.title()} ({len(pokemons)})")
        for pokemon in pokemons:
            st.write(f"- {pokemon.title()}")

with col2:
    
    if selected_type and selected_type != 'Tous':
        try:
            st.subheader(f"📊 Distribution des types pour {selected_type.upper()}")
            
            # Récupération des données
            type_data = requests.get(f"{API_BASE_URL}/pokemon/type/{selected_type}").json()
            df = pd.DataFrame({
                'Statistique': ['Nombre'],
                'Valeur': [len(type_data)]
            })
            
            # Création du graphique
            fig, ax = plt.subplots(figsize=(8,4))
            ax.barh(df['Statistique'], df['Valeur'], color='#EE4045')
            ax.set_title(f"Total: {len(type_data)} Pokémon")
            plt.tight_layout()
            
            st.pyplot(fig)
            
        except Exception as e:
            st.warning(f"Aucune donnée disponible pour {selected_type}")

    # st.subheader("Statistiques des Types")
    # # all_types = requests.get(f"{API_BASE_URL}/types").json()
    # try:
    #     type_response = requests.get(f"{API_BASE_URL}/types")
    #     type_response.raise_for_status()  # Lève une exception pour les codes 4xx/5xx
    #     all_types = type_response.json()
    # except requests.exceptions.RequestException as e:
    #     st.error(f"Erreur de connexion à l'API : {e}")
    
    # all_types = []
    # type_counts = {}
    
    # for t in all_types:
    #     count = len(requests.get(f"{API_BASE_URL}/pokemon/type/{t}").json())
    #     type_counts[t.title()] = count
    
    # df = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Nombre'])
    # fig, ax = plt.subplots()
    # df.sort_values('Nombre', ascending=False).plot.bar(x='Type', y='Nombre', ax=ax)
    # st.pyplot(fig)²   