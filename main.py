import streamlit as st
import pandas as pd
import sys
import os
from geopy.geocoders import Nominatim
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.load_bike_station import load_bike_station_data
from src.balance_analysis import classify_station_balance
from src.route_optimizer import create_nancy_graph, calculate_balancing_routes
from src.map_utils import create_nancy_map, add_bike_stations_to_map
from streamlit_folium import folium_static
import folium

# Step 1: Load the bike station data
def load_data():
    api_key = '06f91bb37651caa12b9199add8c0a32d07c0a268'
    contract_name = 'nancy'
    stations_df = load_bike_station_data(contract_name, api_key)

    if stations_df is None or stations_df.empty:
        st.error("Failed to load bike station data. Please check the API key or internet connection.")
        return pd.DataFrame()
    return stations_df.head(3)  # Limit to only 3 stations for faster loading

# Streamlit UI
st.title("Nancy Bike Station Balancing")
st.write("This application helps manage the bike stations in Nancy by balancing overstocked and understocked stations in real-time.")

# Step 2: Load and classify bike stations
stations_df = load_data()

if not stations_df.empty:
    # Step 3: Classify the stations
    stations_df = classify_station_balance(stations_df)

    # Step 4: Create a map of Nancy with all stations
    nancy_map = create_nancy_map()
    nancy_map = add_bike_stations_to_map(stations_df, nancy_map)

    # Step 5: Get Driver Location using geolocation
    st.sidebar.header("Driver Location")
    geolocator = Nominatim(user_agent="nancy_bike_app")
    location = geolocator.geocode("Nancy, France")
    driver_lat, driver_lng = location.latitude, location.longitude

    # Option to manually input coordinates
    driver_lat = st.sidebar.number_input("Latitude", value=driver_lat, format="%.4f")
    driver_lng = st.sidebar.number_input("Longitude", value=driver_lng, format="%.4f")
    driver_coords = (driver_lat, driver_lng)

    # Step 6: Add driver's current location to the map
    folium.Marker(
        location=[driver_lat, driver_lng],
        popup="Driver's Current Position",
        icon=folium.Icon(color='orange', icon='car', prefix='fa')
    ).add_to(nancy_map)

    # Step 7: Calculate rebalancing routes based on driver location
    G = create_nancy_graph()
    rebalancing_routes = calculate_balancing_routes(G, stations_df, driver_coords)

    # Step 8: Display the rebalancing routes in the UI
    st.header("Rebalancing Routes")
    if rebalancing_routes:
        for route in rebalancing_routes:
            st.write(f"Action: {route['action']} at {route['station_name']}")
    else:
        st.write("No rebalancing routes available at this time.")

    # Step 9: Display the map with bike stations and driver's current position
    folium_static(nancy_map)
else:
    st.stop()  # Stop further execution if the data is not available