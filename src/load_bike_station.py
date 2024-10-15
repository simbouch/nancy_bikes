# src/load_bike_station.py

import pandas as pd
import sys
import os
import streamlit as st  # Importer Streamlit pour accéder aux secrets
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.call_api import get_bike_station_data


def load_bike_station_data() -> pd.DataFrame:
    """
    Charge les données des stations de vélos depuis l'API et les traite dans un DataFrame.

    Utilise le nom du contrat 'nancy' et la clé API intégrée.

    Returns:
        pd.DataFrame: DataFrame contenant les données des stations avec latitude et longitude.
    """
    contract_name = 'nancy'
    api_key = st.secrets["JCDECAUX_API_KEY"]  # Récupérer la clé API depuis secrets.toml
    
    data = get_bike_station_data(contract_name, api_key)
    if data:
        for station in data:
            station['lat'] = station['position']['lat']
            station['lng'] = station['position']['lng']
        stations_df = pd.DataFrame(data)
        return stations_df
    else:
        print("Échec de la récupération des données des stations de vélos.")
        return pd.DataFrame()

# Exemple d'utilisation
if __name__ == "__main__":
    bike_stations_df = load_bike_station_data()
    if not bike_stations_df.empty:
        print(bike_stations_df.head())
    else:
        print("Aucune donnée de stations disponible.")
