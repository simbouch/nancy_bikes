import osmnx as ox
import networkx as nx
import requests
import folium
import time
from Src.call_api import call_api

# Thresholds for "almost empty" and "almost full" (percentages)
almost_empty = 30  # Percentage below which the station is considered almost empty
almost_full = 70   # Percentage above which the station is considered almost full

# Distance threshold (en mètre) to consider two stations as "close"
distance_threshold = 1000  # Par exemple, 1000 mètres

# Récupérer le graphe routier de Nancy via OSMnx
place_name = "Nancy, France"
G = ox.graph_from_place(place_name, network_type='bike')

# Ne garder que le plus grand composant connexe du graphe
G = ox.utils_graph.get_largest_component(G)

# Fonction pour calculer la distance entre deux stations via le réseau routier
def calculate_distance_and_path(station1, station2):
    try:
        # Trouver les nœuds les plus proches des coordonnées des deux stations
        origin_node = ox.distance.nearest_nodes(G, station1['position']['lng'], station1['position']['lat'])
        destination_node = ox.distance.nearest_nodes(G, station2['position']['lng'], station2['position']['lat'])

        # Calculer le chemin le plus court entre les deux nœuds en termes de longueur
        shortest_path = nx.shortest_path(G, origin_node, destination_node, weight='length')

        # Calculer la distance réelle via les routes (pondérée par la longueur)
        distance = nx.shortest_path_length(G, origin_node, destination_node, weight='length')
        return distance, shortest_path
    except nx.NetworkXNoPath:
        return None, None

# Fonction pour convertir les nœuds en coordonnées lat/lng pour afficher le chemin sur la carte
def nodes_to_coordinates(path):
    return [(G.nodes[node]['y'], G.nodes[node]['x']) for node in path]

# Fonction pour mettre à jour et générer la carte avec des données actualisées
def update_map():
    # Appeler l'API pour récupérer les données des stations
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

    # Initialiser les variables pour les statistiques
    total_bikes = 0
    total_stands = 0
    bikes_to_move = 0
    stations_above_full = 0
    empty_stations = 0
    almost_full_stations = 0
    almost_empty_stations = 0

    # Ajouter un marqueur pour chaque station de vélos avec des informations en temps réel et tracer les liaisons
    for i, station in enumerate(stations_data):
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
            almost_full_stations += 1
        if bike_percentage < almost_empty:
            almost_empty_stations += 1

        if bike_percentage > almost_full:
            bikes_to_move += available_bikes
            stations_above_full += 1

            # Calculate bikes to redistribute
            excess_bikes = int((bike_percentage - almost_full) / 100 * total_capacity)
        else:
            excess_bikes = 0

        # Calculer la distance et le chemin à la prochaine station (si applicable)
        if i < len(stations_data) - 1:
            next_station = stations_data[i + 1]
            distance_to_next_station, path = calculate_distance_and_path(station, next_station)
            if distance_to_next_station:
                distance_text = f"<b>Distance à la prochaine station:</b> {round(distance_to_next_station, 2)} m<br>"

                # Si un chemin est trouvé, tracer une ligne entre les deux stations
                path_coords = nodes_to_coordinates(path)

                # Appliquer une ligne en gras si les stations sont proches (moins de "distance_threshold")
                if distance_to_next_station < distance_threshold:
                    folium.PolyLine(locations=path_coords, color="blue", weight=5, opacity=0.9).add_to(mymap)  # Ligne en gras
                else:
                    folium.PolyLine(locations=path_coords, color="blue", weight=2.5, opacity=0.8).add_to(mymap)  # Ligne normale
            else:
                distance_text = "<b>Distance à la prochaine station:</b> Aucun chemin disponible<br>"
        else:
            distance_text = ""

        # Créer un popup avec les informations en temps réel
        popup_text = f"""
        <b>{name}</b><br><br>
        <b>Stands utilisés:</b> {available_bikes} / {total_capacity}<br>
        <i>{available_stands} places libres</i><br>
        {distance_text}
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

    # Add the custom HTML to the map
    from folium.plugins import FloatImage
    html = f"""
        <div style='position: fixed; top: 10px; left: 10px; width: 300px; background-color: white; padding: 10px; z-index: 9999;'>
            <h4><b>Statistiques des stations de vélos</b></h4>
            <ul>
                <li><b>Total vélos :</b> {total_bikes}</li>
                <li><b>Total places libres :</b> {total_stands}</li>
                <li><b>Stations presque pleines :</b> {almost_full_stations} / {len(stations_data)}</li>
                <li><b>Stations presque vides :</b> {almost_empty_stations} / {len(stations_data)}</li>
                <li><b>Stations totalement vides :</b> {empty_stations} / {len(stations_data)}</li>
            </ul> <br>
    
            <h4><b>Infos équilibrage</b></h4>
            <ul>
                <li><b>Vélos à redistribuer :</b> {bikes_to_move}</li>
                <li><b>Stations presque pleines :</b> {stations_above_full} / {len(stations_data)}</li>
            </ul>
        </div>
        """
    mymap.get_root().html.add_child(folium.Element(html))

    # Ajouter un script de rafraîchissement automatique toutes les 60 secondes
    auto_refresh_script = """
    <script type="text/javascript">
        setTimeout(function() {
            location.reload();
        }, 60000);  // Rafraîchit la page toutes les 60 secondes
    </script>
    """
    mymap.get_root().html.add_child(folium.Element(auto_refresh_script))

    # Enregistrer la carte dans un fichier HTML
    mymap.save("nancy_bike_stations_live.html")
    print("Carte mise à jour et enregistrée sous 'nancy_bike_stations_live.html'.")

# Boucle pour mettre à jour la carte toutes les 60 secondes
while True:
    update_map()
    time.sleep(60)