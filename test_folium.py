import requests
import folium
import json
import os
from Src.call_api import call_api

# Thresholds for "almost empty" and "almost full" (percentages)
almost_empty = 30  # Percentage below which the station is considered almost empty
almost_full = 70   # Percentage above which the station is considered almost full

# Margin for balancing
margin_amount = 5  # Number of bikes to be added or removed for balancing

def analyse_stations(stations_data):
    analysed_stations = []

    # Analyze each station and calculate its status, including additional information
    for station in stations_data:
        station_id = station['number']
        name_with_id = station['name']
        name = name_with_id.split(" - ", 1)[1].strip()
        available_bikes = station['available_bikes']
        available_stands = station['available_bike_stands']
        total_capacity = available_bikes + available_stands
        latitude = station['position']['lat']
        longitude = station['position']['lng']

        # Determine station status and bikes to add/remove
        if total_capacity > 0:
            bike_percentage = (available_bikes / total_capacity) * 100
        else:
            bike_percentage = 0

        if available_bikes == 0:
            status = "empty"
            bikes_to_add = max(available_stands, margin_amount)
            bikes_to_remove = 0
        elif bike_percentage < almost_empty:
            status = "almost_empty"
            bikes_needed_for_balance = int((almost_empty - bike_percentage) / 100 * total_capacity)
            bikes_to_add = max(bikes_needed_for_balance, margin_amount)
            bikes_to_remove = 0
        elif bike_percentage > almost_full:
            status = "almost_full"
            bikes_needed_for_balance = int((bike_percentage - almost_full) / 100 * total_capacity)
            bikes_to_add = 0
            bikes_to_remove = bikes_needed_for_balance + margin_amount
        elif available_stands == 0:
            status = "full"
            bikes_to_add = 0
            bikes_to_remove = available_bikes + margin_amount
        else:
            status = "balanced"
            bikes_to_add = 0
            bikes_to_remove = 0

        # Add station data to the list with all the relevant details
        analysed_stations.append({
            'station_id': station_id,
            'name': name,
            'latitude': latitude,
            'longitude': longitude,
            'available_bikes': available_bikes,
            'available_stands': available_stands,
            'total_capacity': total_capacity,
            'status': status,
            'bikes_to_remove': bikes_to_remove,
            'bikes_to_add': bikes_to_add
        })

    # Write or update the json file with all station data
    with open('analysed_stations.json', 'w') as json_file:
        json.dump(analysed_stations, json_file, indent=4)

# Call the API to get bike station data for Nancy
response = call_api('nancy')

# Vérifier si la requête est réussie
if response.status_code == 200:
    stations_data = response.json()
    analyse_stations(stations_data)
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
