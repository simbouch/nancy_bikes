import streamlit as st
import pandas as pd
import sys
import random
from streamlit_folium import folium_static
import folium

# Ajouter le chemin du projet pour importer les modules
sys.path.append('src')

from load_bike_station import load_bike_station_data
from balance_analysis import classify_station_balance
from route_optimizer import create_nancy_graph, find_best_station
from map_utils import create_nancy_map, add_bike_stations_to_map, add_driver_position, add_route_to_map, add_map_legend

def load_data() -> pd.DataFrame:
    """
    Charge les données des stations de vélos.
    """
    stations_df = load_bike_station_data()

    if stations_df.empty:
        st.error("Échec du chargement des données des stations de vélos. Veuillez vérifier la clé API ou la connexion Internet.")
    else:
        if 'number' in stations_df.columns:
            stations_df = stations_df.rename(columns={'number': 'id'})
        elif 'id' not in stations_df.columns:
            stations_df = stations_df.reset_index().rename(columns={'index': 'id'})
    return stations_df

def get_random_position_in_nancy():
    """
    Returns random coordinates within Nancy, France.
    """
    # Approximate coordinates boundaries of Nancy, France
    lat = random.uniform(48.65, 48.72)
    lon = random.uniform(6.15, 6.20)
    return lat, lon

def main():
    # Configuration de la page Streamlit
    st.set_page_config(page_title="Nancy Bike Station Rebalancing", layout="wide")

    # Titre et description de l'application
    st.title("🚴‍♂️ Rééquilibrage des Stations de Vélos à Nancy 🚴‍♀️")
    st.markdown("""
        Cette application vous aide à gérer les stations de vélos à Nancy en rééquilibrant les stations surchargées et sous-alimentées en temps réel.
        Suivez les étapes suivantes pour obtenir un itinéraire optimisé :
        1. **Affichage des Stations :** Visualisez les stations de vélos sur la carte.
        2. **Localisation du Conducteur :** La position du conducteur est générée aléatoirement à Nancy.
        3. **Action à Entreprendre :** Sélectionnez l'action (Collecter ou Déposer des vélos).
        4. **Calculer l'Itinéraire :** Obtenez l'itinéraire optimisé.
        5. **Visualiser l'Itinéraire :** Visualisez l'itinéraire sur la carte avec les détails.
    """)

    # Charger et classer les données des stations
    stations_df = load_data()
    if not stations_df.empty:
        stations_df = classify_station_balance(stations_df)

        # Position aléatoire du conducteur dans Nancy
        driver_coords = get_random_position_in_nancy()

        # Créer la carte initiale avec les stations et la position du conducteur
        nancy_map = create_nancy_map()
        nancy_map = add_bike_stations_to_map(stations_df, nancy_map)
        nancy_map = add_driver_position(nancy_map, driver_coords)

        # Afficher la carte initiale avec les stations
        st.header("🗺️ Carte des Stations de Vélos et Position du Conducteur")
        folium_static(nancy_map, width=950, height=650)

        # Choix de l'action (menu déroulant en français)
        action = st.selectbox("Sélectionner l'action", ("Collecter", "Déposer"))

        # Bouton pour calculer l'itinéraire
        if st.button("✨ Calculer l'itinéraire"):
            with st.spinner("Calcul en cours..."):
                try:
                    # Créer le graphe réseau routier de Nancy
                    G = create_nancy_graph()
                    best_action = find_best_station(G, driver_coords, stations_df, 'collect' if action == 'Collecter' else 'deposit')

                    if best_action:
                        # Créer la carte avec l'itinéraire
                        nancy_map = create_nancy_map()
                        nancy_map = add_bike_stations_to_map(stations_df, nancy_map)
                        nancy_map = add_driver_position(nancy_map, driver_coords)

                        # Ajouter l'itinéraire à la carte
                        nancy_map = add_route_to_map(nancy_map, G, best_action['path'], color='blue' if action == 'Collecter' else 'green')

                        # Ajouter la légende à la carte
                        nancy_map = add_map_legend(nancy_map)

                        # Afficher la carte mise à jour avec l'itinéraire
                        st.header("🛣️ Carte avec Itinéraire Optimisé")
                        folium_static(nancy_map, width=960, height=600)

                        # Afficher les détails de la station
                        st.subheader("📄 Détails de la Station Sélectionnée")
                        station_name = best_action['station_name'].split(' - ', 1)[-1] if ' - ' in best_action['station_name'] else best_action['station_name']
                        st.write(f"**Station:** {station_name}")
                        st.write(f"**Action:** {action}")
                        st.write(f"**Distance:** {best_action['distance_m']:.2f} mètres")
                        st.write(f"**Nombre de vélos dans la station:** {best_action['bikes']}")

                        st.success("Itinéraire optimisé calculé avec succès ! 🎉")
                    else:
                        st.info(f"Aucune station appropriée trouvée pour l'action '{action}'.")
                except Exception as e:
                    st.error(f"Une erreur est survenue lors du calcul de l'itinéraire : {e}")

if __name__ == "__main__":
    main()
