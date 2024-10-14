import pandas as pd

# Classification des stations de vélos
# Classe chaque station comme surchargée, sous-alimentée ou équilibrée
def classify_station_balance(stations_df):
    stations_df['balance_status'] = stations_df.apply(
        lambda x: 'overstocked' if x['available_bikes'] > x['bike_stands'] * 0.7
        else ('understocked' if x['available_bikes'] < x['bike_stands'] * 0.3 else 'balanced'), axis=1
    )
    return stations_df