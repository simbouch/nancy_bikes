# src/balance_analysis.py

import pandas as pd

def classify_station_balance(stations_df: pd.DataFrame) -> pd.DataFrame:
    """
    Classe le statut de balance de chaque station basé sur les vélos disponibles et les emplacements disponibles.

    Args:
        stations_df (pd.DataFrame): DataFrame contenant les données des stations de vélos.

    Returns:
        pd.DataFrame: DataFrame avec les colonnes supplémentaires 'balance_status' et 'available_bike_stands'.
    """
    def balance_status(row):
        capacity = row['bike_stands']
        available = row['available_bikes']
        available_stands = capacity - available
        row['available_bike_stands'] = available_stands
        if available > capacity * 0.8:
            return 'overstocked'
        elif available < capacity * 0.2:
            return 'understocked'
        else:
            return 'balanced'

    stations_df = stations_df.copy()
    stations_df['balance_status'] = stations_df.apply(balance_status, axis=1)
    return stations_df
