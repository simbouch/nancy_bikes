# app.py

import streamlit as st
import pandas as pd
import sys
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium

# Ajouter le chemin du projet pour importer les modules
sys.path.append('src')  # Correction ici

from load_bike_station import load_bike_station_data
from balance_analysis import classify_station_balance
from route_optimizer import create_nancy_graph, find_best_station
from map_utils import create_nancy_map, add_bike_stations_to_map, add_driver_position, add_route_to_map, add_map_legend

def load_data() -> pd.DataFrame:
    """
    Charge les données des stations de vélos.

    Returns:
        pd.DataFrame: DataFrame contenant les données des stations de vélos.
    """
    stations_df = load_bike_station_data()

    if stations_df.empty:
        st.error("Échec du chargement des données des stations de vélos. Veuillez vérifier la clé API ou la connexion Internet.")
    else:
        # Si l'API fournit des identifiants uniques, utilisez-les. Sinon, créez-les.
        if 'number' in stations_df.columns:
            stations_df = stations_df.rename(columns={'number': 'id'})
        elif 'id' not in stations_df.columns:
            stations_df = stations_df.reset_index().rename(columns={'index': 'id'})
    return stations_df

def main():
    # Titre et description de l'application
    st.title("Rééquilibrage des Stations de Vélos à Nancy")
    st.write("""
        Cette application vous aide à gérer les stations de vélos à Nancy en rééquilibrant les stations surchargées et sous-alimentées en temps réel.
        Suivez les étapes suivantes pour obtenir un itinéraire optimisé :
        1. **Affichage des Stations :** Visualisez les stations de vélos sur la carte.
        2. **Paramètres du Véhicule :** Entrez la capacité de votre véhicule et le nombre de vélos actuellement dans le véhicule.
        3. **Calculer l'Itinéraire :** L'application déterminera automatiquement la meilleure station pour collecter ou déposer des vélos.
        4. **Visualiser l'Itinéraire :** Visualisez l'itinéraire optimisé sur la carte avec les informations détaillées des stations.
    """)

    # Charger et classer les données des stations
    stations_df = load_data()
    if not stations_df.empty:
        stations_df = classify_station_balance(stations_df)

        # Créer la carte et ajouter les stations
        nancy_map = create_nancy_map()
        nancy_map = add_bike_stations_to_map(stations_df, nancy_map)

        # Localisation du conducteur
        st.sidebar.header("Localisation du Conducteur")
        geolocator = Nominatim(user_agent="nancy_bike_app")
        default_location = geolocator.geocode("Nancy, France")
        if default_location:
            driver_lat, driver_lng = default_location.latitude, default_location.longitude
        else:
            st.sidebar.error("Impossible de localiser Nancy, France.")
            driver_lat, driver_lng = 48.6844, 6.1844  # Coordonnées de repli

        # Options d'entrée manuelle pour latitude et longitude
        driver_lat = st.sidebar.number_input("Latitude", value=driver_lat, format="%.6f")
        driver_lng = st.sidebar.number_input("Longitude", value=driver_lng, format="%.6f")
        driver_coords = (driver_lat, driver_lng)

        # Ajouter la position du conducteur à la carte
        nancy_map = add_driver_position(nancy_map, driver_coords)

        # Afficher la carte avec les stations et la position du conducteur
        st.header("Carte des Stations de Vélos et Position du Conducteur")
        folium_static(nancy_map, width=700, height=500)

        # Paramètres du véhicule
        st.sidebar.header("Paramètres du Véhicule")
        vehicle_capacity = st.sidebar.number_input("Capacité du Véhicule", min_value=1, max_value=20, value=10, step=2)
        current_load = st.sidebar.number_input("Vélos Actuels dans le Véhicule", min_value=0, max_value=vehicle_capacity, value=0, step=1)

        # Choix de l'action
        st.sidebar.header("Action à Entreprendre")
        action = st.sidebar.selectbox("Sélectionner l'action", ("collect", "deposit"))

        # Calculer les itinéraires de rééquilibrage
        st.sidebar.header("Calculer l'Itinéraire")
        if st.sidebar.button("Calculer l'itinéraire"):
            with st.spinner("Calcul en cours..."):
                # Créer le graphe réseau routier de Nancy
                G = create_nancy_graph()
                best_action = find_best_station(G, driver_coords, stations_df, action, vehicle_capacity, current_load)

                if best_action:
                    # Ajouter l'itinéraire à la carte
                    nancy_map = add_route_to_map(nancy_map, G, best_action['path'], color='blue' if action == 'collect' else 'green')
                    print(best_action['path'])
                    print('alloha')
                    # Ajouter la légende à la carte
                    nancy_map = add_map_legend(nancy_map)
                    # Afficher la carte mise à jour avec l'itinéraire
                    st.header("Carte avec Itinéraire Optimisé")
                    folium_static(nancy_map, width=700, height=500)

                    # Afficher les détails de l'itinéraire
                    st.header("Détails de l'Itinéraire")
                    st.markdown(f"### {action.capitalize()} à **{best_action['station_name']}**")
                    st.write(f"**Distance** : {best_action['distance_m']:.2f} mètres")
                    st.write(f"**Vélos** : {best_action['bikes']}")

                else:
                    st.info(f"Aucune station appropriée trouvée pour l'action '{action}'.")
        
        # Option de rafraîchissement des données
        st.sidebar.header("Actualiser les Données")
        if st.sidebar.button("Actualiser"):
            st.experimental_rerun()

if __name__ == "__main__":
    main()
