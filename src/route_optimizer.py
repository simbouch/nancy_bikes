# src/route_optimizer.py

import networkx as nx
import osmnx as ox
import pandas as pd
from typing import List, Dict, Tuple, Optional

def create_nancy_graph() -> nx.MultiDiGraph:
    """
    Crée un graphe réseau routier de Nancy en utilisant OSMnx.

    Returns:
        nx.MultiDiGraph: Graphe réseau routier de Nancy.
    """
    return ox.graph_from_place("Nancy, France", network_type='drive')

def find_nearest_node(G: nx.MultiDiGraph, coords: Tuple[float, float]) -> int:
    """
    Trouve le nœud le plus proche dans le graphe pour les coordonnées données.

    Args:
        G (nx.MultiDiGraph): Graphe réseau routier.
        coords (Tuple[float, float]): (latitude, longitude).

    Returns:
        int: ID du nœud le plus proche.
    """
    return ox.distance.nearest_nodes(G, coords[1], coords[0])

def calculate_distance(G: nx.MultiDiGraph, source_coords: Tuple[float, float], target_coords: Tuple[float, float]) -> Optional[float]:
    """
    Calcule la distance la plus courte entre deux coordonnées.

    Args:
        G (nx.MultiDiGraph): Graphe réseau routier.
        source_coords (Tuple[float, float]): (latitude, longitude) de la source.
        target_coords (Tuple[float, float]): (latitude, longitude) de la cible.

    Returns:
        Optional[float]: Distance en mètres ou None s'il n'y a pas de chemin.
    """
    try:
        source_node = find_nearest_node(G, source_coords)
        target_node = find_nearest_node(G, target_coords)
        distance = nx.shortest_path_length(G, source=source_node, target=target_node, weight='length')
        return distance
    except nx.NetworkXNoPath:
        return None

def find_best_station(
    G: nx.MultiDiGraph,
    driver_coords: Tuple[float, float],
    stations_df: pd.DataFrame,
    action: str,  # 'collect' ou 'deposit'
    vehicle_capacity: int,
    current_load: int
) -> Optional[Dict]:
    """
    Trouve la meilleure station pour collecter ou déposer des vélos.

    Args:
        G (nx.MultiDiGraph): Graphe réseau routier.
        driver_coords (Tuple[float, float]): (latitude, longitude) actuel du conducteur.
        stations_df (pd.DataFrame): DataFrame contenant les données des stations de vélos.
        action (str): 'collect' ou 'deposit'.
        vehicle_capacity (int): Capacité du véhicule.
        current_load (int): Nombre actuel de vélos dans le véhicule.

    Returns:
        Optional[Dict]: Dictionnaire contenant les détails de l'action ou None si aucune station appropriée n'est trouvée.
    """
    # Filtrer les stations en fonction de l'action
    if action == 'collect':
        suitable_stations = stations_df[stations_df['balance_status']=='overstocked']
    elif action == 'deposit':
        suitable_stations = stations_df[stations_df['balance_status']=='understocked']
    else:
        raise ValueError("L'action doit être 'collect' ou 'deposit'.")

    if suitable_stations.empty:
        return None

    # Calculer les distances
    suitable_stations['distance'] = suitable_stations.apply(
        lambda row: calculate_distance(G, driver_coords, (row['lat'], row['lng'])) or float('inf'),
        axis=1
    )

    # Filtrer les stations accessibles
    suitable_stations = suitable_stations[suitable_stations['distance'] != float('inf')]

    if suitable_stations.empty:
        return None

    # Calculer le score en fonction de l'action
    if action == 'collect':
        # Prioriser les stations proches avec le plus de vélos disponibles
        suitable_stations['score'] = suitable_stations['available_bikes'] / (suitable_stations['distance'] + 1)
    elif action == 'deposit':
        # Prioriser les stations proches avec le plus d'emplacements disponibles
        suitable_stations['score'] = suitable_stations['available_bike_stands'] / (suitable_stations['distance'] + 1)

    # Trouver la station avec le meilleur score
    best_station = suitable_stations.loc[suitable_stations['score'].idxmax()]

    # Calculer le chemin
    path = nx.shortest_path(
        G,
        source=find_nearest_node(G, driver_coords),
        target=find_nearest_node(G, (best_station['lat'], best_station['lng'])),
        weight='length'
    )

    # Déterminer le nombre de vélos à collecter ou déposer
    if action == 'collect':
        bikes = min(vehicle_capacity - current_load, best_station['available_bikes'])
    else:  # 'deposit'
        bikes = min(current_load, best_station['available_bike_stands'])

    return {
        'action': action,
        'station_id': best_station['id'],
        'station_name': best_station['name'],
        'from': driver_coords,
        'to': (best_station['lat'], best_station['lng']),
        'distance_m': best_station['distance'],
        'bikes': bikes,
        'path': path
    }
