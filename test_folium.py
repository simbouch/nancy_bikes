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

# Ajouter un marqueur pour chaque station de vélos avec des informations en temps réel
for station in stations_data:
    lat = station['position']['lat']
    lng = station['position']['lng']
    name_with_id = station['name']

    # Remove the ID by splitting on the first hyphen and stripping any extra spaces
    name = name_with_id.split(" - ", 1)[1].strip()

    available_bikes = station['available_bikes']
    available_stands = station['available_bike_stands']
    total_capacity = available_bikes + available_stands  # Calculating total capacity

    # Calculate the percentage of available bikes
    if total_capacity > 0:
        bike_percentage = (available_bikes / total_capacity) * 100
    else:
        bike_percentage = 0

    # Créer un popup avec les informations en temps réel, avec une largeur plus large
    popup_text = f"""
    <b>{name}</b><br><br>
    <b>Vélos disponibles:</b> {available_bikes}<br>
    <b>Places libres:</b> {available_stands}<br>
    <b>Capacité totale:</b> {total_capacity}
    """

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

# Enregistrer la carte dans un fichier HTML
mymap.save("nancy_bike_stations_live.html")

print("Carte enregistrée sous 'nancy_bike_stations_live.html'. Ouvrez ce fichier pour afficher la carte.")
