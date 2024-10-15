# src/map_utils.py

import folium
import pandas as pd
from folium import Marker, Icon, Popup
from folium.plugins import MarkerCluster
import networkx as nx
from typing import Tuple, List

def create_nancy_map() -> folium.Map:
    """
    Crée une carte Folium centrée sur Nancy, France.

    Returns:
        folium.Map: Objet carte Folium centré sur Nancy.
    """
    nancy_coords = [48.6844, 6.1844]
    return folium.Map(location=nancy_coords, zoom_start=13)

def add_bike_stations_to_map(stations_df: pd.DataFrame, nancy_map: folium.Map) -> folium.Map:
    """
    Ajoute les marqueurs des stations de vélos à la carte Folium avec des informations en français.

    Args:
        stations_df (pd.DataFrame): DataFrame contenant les données des stations de vélos.
        nancy_map (folium.Map): Objet carte Folium auquel ajouter les marqueurs.

    Returns:
        folium.Map: Carte Folium mise à jour avec les marqueurs des stations de vélos.
    """
    marker_cluster = MarkerCluster().add_to(nancy_map)

    for _, station in stations_df.iterrows():
        popup_content = (
            f"<b>Station:</b> {station['name']}<br>"
            f"<b>Vélos Disponibles:</b> {station['available_bikes']}<br>"
            f"<b>Emplacements Disponibles:</b> {station['available_bike_stands']}<br>"
            f"<b>Statut:</b> {station['balance_status'].capitalize()}"
        )
        
        # Déterminer la couleur du marqueur en fonction du statut de balance
        if station['balance_status'] == 'balanced':
            color = 'blue'
        elif station['balance_status'] == 'understocked':
            color = 'green'
        else:
            color = 'red'
        
        marker = Marker(
            location=[station['lat'], station['lng']],
            popup=Popup(popup_content, max_width=300),
            icon=Icon(color=color, icon='bicycle', prefix='fa')
        )
        marker.add_to(marker_cluster)
    return nancy_map

def add_driver_position(nancy_map: folium.Map, driver_coords: Tuple[float, float]) -> folium.Map:
    """
    Ajoute la position actuelle du conducteur à la carte Folium.

    Args:
        nancy_map (folium.Map): Objet carte Folium.
        driver_coords (Tuple[float, float]): (latitude, longitude) du conducteur.

    Returns:
        folium.Map: Carte Folium mise à jour avec la position du conducteur.
    """
    folium.Marker(
        location=[driver_coords[0], driver_coords[1]],
        popup="Position Actuelle du Conducteur",
        icon=Icon(color='orange', icon='car', prefix='fa')
    ).add_to(nancy_map)
    return nancy_map

def add_route_to_map(nancy_map: folium.Map, G: nx.MultiDiGraph, route: List[int], color: str = 'blue') -> folium.Map:
    """
    Ajoute un itinéraire à la carte sous forme de polyligne avec un tooltip indiquant la distance.

    Args:
        nancy_map (folium.Map): Objet carte Folium.
        G (nx.MultiDiGraph): Graphe réseau routier.
        route (List[int]): Liste des IDs de nœuds représentant l'itinéraire.
        color (str, optional): Couleur de la polyligne. Defaults to 'blue'.

    Returns:
        folium.Map: Carte Folium mise à jour avec l'itinéraire.
    """
    if not route:
        return nancy_map
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    # Calculer la distance totale
    total_distance = sum(
        G.edges[route[i], route[i+1], 0]['length'] for i in range(len(route)-1)
    )
    folium.PolyLine(
        locations=route_coords,
        color=color,
        weight=4,
        opacity=0.7,
        tooltip=f"Distance: {total_distance:.2f} m"
    ).add_to(nancy_map)
    return nancy_map

def add_map_legend(nancy_map: folium.Map) -> folium.Map:
    """
    Ajoute une légende à la carte Folium expliquant les codes couleur des stations.

    Args:
        nancy_map (folium.Map): Objet carte Folium.

    Returns:
        folium.Map: Carte Folium mise à jour avec une légende.
    """
    legend_html = '''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 160px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white;
     padding: 10px;
     ">
     <h4>Légende des Statuts</h4>
     <i class="fa fa-bicycle" style="color:red"></i>&nbsp;Surchargé<br>
     <i class="fa fa-bicycle" style="color:green"></i>&nbsp;Sous-alimenté<br>
     <i class="fa fa-bicycle" style="color:blue"></i>&nbsp;Équilibré<br>
     <i class="fa fa-car" style="color:orange"></i>&nbsp;Conducteur
     </div>
     '''
    folium.Element(legend_html).add_to(nancy_map)
    return nancy_map
