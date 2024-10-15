import requests
import folium
import json
import os

from src.call_api import call_api
from src.data_analysis import analyse_stations

# Thresholds for "almost empty" and "almost full" (percentages)
almost_empty = 30  # Percentage below which the station is considered almost empty
almost_full = 70   # Percentage above which the station is considered almost full

# Margin for balancing
margin_amount = 5  # Number of bikes to be added or removed for balancing

# Call the API to get bike station data for Nancy
response = call_api('nancy')

# Vérifier si la requête est réussie
if response.status_code == 200:
    stations_data = response.json()
    # Pass almost_empty, almost_full, and margin_amount as arguments
    analyse_stations(stations_data, almost_empty, almost_full, margin_amount)
else:
    print("Erreur lors de la récupération des données :", response.status_code)
    stations_data = []

# Créer une carte centrée sur Nancy
nancy_coords = [48.692054, 6.184417]
mymap = folium.Map(location=nancy_coords, zoom_start=13)

# Load the analysed station data from the json file
if os.path.exists('analysed_stations.json'):
    with open('analysed_stations.json', 'r') as json_file:
        analysed_stations = json.load(json_file)
else:
    analysed_stations = []

# Loop over the analysed stations and create the map markers
for station in analysed_stations:
    lat = station['latitude']
    lng = station['longitude']

    # Create a popup with all the analyzed data
    popup_text = f"""
    <b>{station['name']}</b><br>
    <br>
    <b>Stands utilisés:</b> {station['available_bikes']} / {station['total_capacity']}<br>
    <i>{station['available_stands']} places libres</i>
    """

    # Add the 'Equilibrage' section only if the station is not balanced
    if station['bikes_to_add'] > 0 or station['bikes_to_remove'] > 0:
        popup_text += "<br><br><b>Equilibrage</b><br>"
        if station['bikes_to_remove'] > 0:
            popup_text += f"<b>Vélos à retirer:</b> {station['bikes_to_remove']}<br>"
        if station['bikes_to_add'] > 0:
            popup_text += f"<b>Vélos à ajouter:</b> {station['bikes_to_add']}<br>"

    # Folium's Popup allows you to set the maximum width (in pixels)
    popup = folium.Popup(popup_text, max_width=300)

    # Color logic based on station status
    if station['status'] == 'empty':
        marker_color = 'lightgray'
    elif station['status'] == 'almost_empty':
        marker_color = 'blue'
    elif station['status'] == 'balanced':
        marker_color = 'green'
    elif station['status'] == 'almost_full':
        marker_color = 'orange'
    elif station['status'] == 'full':
        marker_color = 'red'

    # Ajouter un marqueur avec un popup
    folium.Marker(
        location=[lat, lng],
        popup=popup,
        icon=folium.Icon(color=marker_color)
    ).add_to(mymap)

# Calculate statistics for display
total_bikes = sum(s['available_bikes'] for s in analysed_stations)
total_stands = sum(s['available_stands'] for s in analysed_stations)
total_capacity = sum(s['available_bikes'] + s['available_stands'] for s in analysed_stations)  # Fix for total capacity
num_stations = len(analysed_stations)
stations_above_full = sum(1 for s in analysed_stations if s['status'] == 'almost_full')
full_stations = sum(1 for s in analysed_stations if s['status'] == 'full')
stations_almost_empty = sum(1 for s in analysed_stations if s['status'] == 'almost_empty')
empty_stations = sum(1 for s in analysed_stations if s['status'] == 'empty')
bikes_to_move = sum(s['bikes_to_remove'] for s in analysed_stations)

# Create the custom HTML to show on the map
html = f"""
    <div style='position: fixed; top: 10px; left: 10px; width: 300px; background-color: white; padding: 10px; z-index: 9999;'>
        <h4><b>Statistiques des stations de vélos</b></h4>
        <ul>
            <li><b>Total vélos :</b> {total_bikes}</li>
            <li><b>Total places libres :</b> {total_stands} / {total_capacity}</li>
        </ul> <br>

        <h4><b>Infos équilibrage</b></h4>
        <ul>
            <li><b>Total stations :</b> {num_stations}</li>
            <li><b>Vélos à redistribuer :</b> {bikes_to_move}</li>
            <li><b>Stations à vider :</b> {stations_above_full} / {num_stations}</li>
            <li><b>Stations pleines :</b> {full_stations} / {num_stations}</li>
            <li><b>Stations à remplir :</b> {stations_almost_empty} / {num_stations}</li>
            <li><b>Stations vides :</b> {empty_stations} / {num_stations}</li> <br>
        </ul>

        <h4><b>Redistribution</b></h4>
        <a href="redistribution_path.html">Démarrer l'équilibrage</a> <br> <br>

        <h4><b>Mon camion</b></h4>
        <ul>
            <li><b>Remplissage :</b> 8 / 20 </li>
        </ul>
    </div>
"""

# Add the custom HTML to the map
mymap.get_root().html.add_child(folium.Element(html))

# Enregistrer la carte dans un fichier HTML
mymap.save("nancy_bike_stations_live.html")

print("Carte enregistrée sous 'nancy_bike_stations_live.html'. Ouvrez ce fichier pour afficher la carte.")
