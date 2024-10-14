import requests
import folium
from Src.call_api import call_api

# Thresholds for "almost empty" and "almost full" (percentages)
almost_empty = 30  # Percentage below which the station is considered almost empty
almost_full = 70   # Percentage above which the station is considered almost full

# Call the API to get bike station data for Nancy
response = call_api('nancy')

# Vérifier si la requête est réussie
if response.status_code == 200:
    stations_data = response.json()
else:
    print("Erreur lors de la récupération des données :", response.status_code)
    stations_data = []

# Créer une carte centrée sur Nancy
nancy_coords = [48.692054, 6.184417]
mymap = folium.Map(location=nancy_coords, zoom_start=13)

# Initialize variables for statistics
total_bikes = 0
total_stands = 0
bikes_to_move = 0
stations_above_full = 0
empty_stations = 0

# Loop over the stations to populate the map and calculate statistics
for station in stations_data:
    lat = station['position']['lat']
    lng = station['position']['lng']
    name_with_id = station['name']

    # Remove the ID by splitting on the first hyphen and stripping any extra spaces
    name = name_with_id.split(" - ", 1)[1].strip()

    available_bikes = station['available_bikes']
    available_stands = station['available_bike_stands']
    total_capacity = available_bikes + available_stands  # Calculating total capacity

    # Update the statistics
    total_bikes += available_bikes
    total_stands += available_stands

    if available_bikes == 0:
        empty_stations += 1
    if total_capacity > 0:
        bike_percentage = (available_bikes / total_capacity) * 100
    else:
        bike_percentage = 0

    if bike_percentage > almost_full:
        bikes_to_move += available_bikes
        stations_above_full += 1

        # Calculate bikes to redistribute
        excess_bikes = int((bike_percentage - almost_full) / 100 * total_capacity)
    else:
        excess_bikes = 0

    # Créer un popup avec les informations en temps réel
    popup_text = f"""
    <b>{name}</b><br><br>
    <b>Stands utilisés:</b> {available_bikes} / {total_capacity}<br>
    <i>{available_stands} places libres</i><br>
    """

    # Add 'Vélos à redistribuer' if there are excess bikes
    if excess_bikes > 0:
        popup_text += f"<br><b>Vélos à redistribuer:</b> {excess_bikes}<br>"

    # Folium's Popup allows you to set the maximum width (in pixels)
    popup = folium.Popup(popup_text, max_width=300)

    # Color logic based on station status
    if available_bikes == 0:
        marker_color = 'lightgray'  # Station empty
    elif available_stands == 0:
        marker_color = 'red'  # Station full
    elif bike_percentage < almost_empty:
        marker_color = 'blue'  # Station almost empty
    elif bike_percentage > almost_full:
        marker_color = 'orange'  # Station almost full
    else:
        marker_color = 'green'  # Station in between almost_empty and almost_full

    # Ajouter un marqueur avec un popup
    folium.Marker(
        location=[lat, lng],
        popup=popup,
        icon=folium.Icon(color=marker_color)
    ).add_to(mymap)

# Calculate percentages for statistics
num_stations = len(stations_data)
empty_station_percentage = (empty_stations / num_stations) * 100 if num_stations > 0 else 0
full_station_percentage = (stations_above_full / num_stations) * 100 if num_stations > 0 else 0

# Create the custom HTML to show on the map
html = f"""
    <div style='position: fixed; top: 10px; left: 10px; width: 300px; background-color: white; padding: 10px; z-index: 9999;'>
        <h4><b>Statistiques des stations de vélos</b></h4>
        <ul>
            <li><b>Total vélos :</b> {total_bikes}</li>
            <li><b>Total places libres :</b> {total_stands}</li>
            <li><b>Total places libres :</b> {total_capacity}</li>
        </ul> <br>

        <h4><b>Infos equilibrage</b></h4>
        <ul>
            <li><b>Vélos à redistribuer :</b> {bikes_to_move}</li>
            <li><b>Stations presque pleines :</b> {stations_above_full} / {num_stations}</li>
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
from folium.plugins import FloatImage
mymap.get_root().html.add_child(folium.Element(html))

# Enregistrer la carte dans un fichier HTML
mymap.save("nancy_bike_stations_live.html")

print("Carte enregistrée sous 'nancy_bike_stations_live.html'. Ouvrez ce fichier pour afficher la carte.")
