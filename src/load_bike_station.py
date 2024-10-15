import os
import pandas as pd
import streamlit as st
from call_api import get_bike_station_data

def load_bike_station_data() -> pd.DataFrame:
    """
    Charge les données des stations de vélos depuis l'API et les traite dans un DataFrame.

    Utilise le nom du contrat 'nancy' et la clé API stockée dans secrets.toml ou en environnement.
    """
    contract_name = 'nancy'
    try:
        # Use st.secrets if running with Streamlit
        api_key = st.secrets["secrets"]["JCDECAUX_API_KEY"]
    except KeyError:
        # Fallback to environment variable if running without Streamlit
        api_key = os.getenv("JCDECAUX_API_KEY", "your_backup_api_key")
    
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

if __name__ == "__main__":
    bike_stations_df = load_bike_station_data()
    if not bike_stations_df.empty:
        print(bike_stations_df.head())
    else:
        print("Aucune donnée de stations disponible.")
import toml

# Load secrets from the .streamlit/secrets.toml file
secrets = toml.load(".streamlit/secrets.toml")
print(secrets["secrets"]["JCDECAUX_API_KEY"])
