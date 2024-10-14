import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.call_api import get_bike_station_data

# Charger les données des stations de vélos via l'API
def load_bike_station_data(contract_name, api_key):
    data = get_bike_station_data(contract_name, api_key)
    if data is not None:
        # Extract relevant data and add lat/lng columns
        for station in data:
            station['lat'] = station['position']['lat']
            station['lng'] = station['position']['lng']
        
        # Convert to DataFrame
        stations_df = pd.DataFrame(data)
        return stations_df
    else:
        print("Échec de la récupération des données des stations de vélos.")
        return pd.DataFrame()

if __name__ == "__main__":
    contract_name = 'nancy'
    api_key = '06f91bb37651caa12b9199add8c0a32d07c0a268'
    
    # Charger les données des stations
    stations_df = load_bike_station_data(contract_name, api_key)
    if not stations_df.empty:
        print(stations_df.head())
    else:
        print("Aucune donnée de stations disponible.")
