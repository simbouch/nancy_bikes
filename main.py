import streamlit as st
import pandas as pd
import sys
import os
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium

# Add project path for importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.load_bike_station import load_bike_station_data
from src.balance_analysis import classify_station_balance
from src.route_optimizer import create_nancy_graph, calculate_balancing_routes
from src.map_utils import create_nancy_map, add_bike_stations_to_map

# Step 1: Load bike station data
def load_data():
    api_key = '06f91bb37651caa12b9199add8c0a32d07c0a268'
    contract_name = 'nancy'
    stations_df = load_bike_station_data(contract_name, api_key)

    if stations_df is None or stations_df.empty:
        st.error("Échec du chargement des données des stations de vélos. Veuillez vérifier la clé API ou la connexion Internet.")
        return pd.DataFrame()
    return stations_df.head(3)  # Limit to 3 stations for faster loading

# Step 2: UI title and description
st.title("Rééquilibrage des Stations de Vélos à Nancy")
st.write("Cette application vous aide à gérer les stations de vélos à Nancy en rééquilibrant les stations surchargées et sous-alimentées en temps réel.")

# Step 3: Load and classify stations
stations_df = load_data()
if not stations_df.empty:
    stations_df = classify_station_balance(stations_df)

    # Step 4: Create the Nancy map and add stations
    nancy_map = create_nancy_map()
    nancy_map = add_bike_stations_to_map(stations_df, nancy_map)

    # Step 5: Get driver's location
    st.sidebar.header("Localisation du Conducteur")
    geolocator = Nominatim(user_agent="nancy_bike_app")
    location = geolocator.geocode("Nancy, France")
    driver_lat, driver_lng = location.latitude, location.longitude

    # Option for manual latitude/longitude
    driver_lat = st.sidebar.number_input("Latitude", value=driver_lat, format="%.4f")
    driver_lng = st.sidebar.number_input("Longitude", value=driver_lng, format="%.4f")
    driver_coords = (driver_lat, driver_lng)

    # Step 6: Add driver's current location to the map
    folium.Marker(
        location=[driver_lat, driver_lng],
        popup="Position Actuelle du Conducteur",
        icon=folium.Icon(color='orange', icon='car', prefix='fa')
    ).add_to(nancy_map)

    # Step 7: Create Nancy graph and calculate rebalancing routes
    st.sidebar.header("Calcul des Itinéraires de Rééquilibrage")
    if st.sidebar.button("Calculer l'itinéraire"):
        st.write("Calcul en cours...")

        # Create Nancy road network graph
        G = create_nancy_graph()
        rebalancing_routes = calculate_balancing_routes(G, stations_df, driver_coords)

        # Step 8: Add rebalancing routes to the map
        if rebalancing_routes:
            for route in rebalancing_routes:
                folium.PolyLine(
                    locations=[driver_coords, (route['to'][0], route['to'][1])],
                    color='blue',
                    weight=2.5,
                    opacity=1
                ).add_to(nancy_map)

            # Display rebalancing routes details
            st.header("Itinéraires de Rééquilibrage")
            for route in rebalancing_routes:
                st.write(f"Action : {route['action']} à {route['station_name']}")
        else:
            st.write("Aucun itinéraire de rééquilibrage disponible pour le moment.")

    # Step 9: Display the updated map
    st.header("Carte des Stations et Position du Conducteur")
    folium_static(nancy_map)
else:
    st.stop()
