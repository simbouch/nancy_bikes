import networkx as nx
import osmnx as ox

# Créer un graphe du réseau routier à Nancy
def create_nancy_graph():
    """Creates a road network graph of Nancy using OSMnx."""
    return ox.graph_from_place("Nancy, France", network_type='drive')

# Trouver la station la plus proche du point actuel
def find_closest_station(G, current_coords, stations_df):
    current_node = ox.distance.nearest_nodes(G, current_coords[1], current_coords[0])
    min_distance = float('inf')
    closest_station = None

    for _, station in stations_df.iterrows():
        station_coords = (station['lat'], station['lng'])
        station_node = ox.distance.nearest_nodes(G, station_coords[1], station_coords[0])
        try:
            distance = nx.shortest_path_length(G, current_node, station_node, weight='length')
            if distance < min_distance:
                min_distance = distance
                closest_station = station
        except nx.NetworkXNoPath:
            continue

    return closest_station

# Calculer les chemins pour rééquilibrer les vélos en tenant compte de la capacité du véhicule
def calculate_balancing_routes(G, stations_df, current_coords, vehicle_capacity=10):
    overstocked_stations = stations_df[stations_df['balance_status'] == 'overstocked']
    understocked_stations = stations_df[stations_df['balance_status'] == 'understocked']

    # Trier les stations par ordre de sur/sous-alimentation pour une meilleure priorisation
    overstocked_stations = overstocked_stations.sort_values(by='available_bikes', ascending=False)
    understocked_stations = understocked_stations.sort_values(by='available_bikes')

    rebalancing_routes = []
    current_bike_load = 0

    while not overstocked_stations.empty or not understocked_stations.empty:
        if current_bike_load < vehicle_capacity and not overstocked_stations.empty:
            closest_station = find_closest_station(G, current_coords, overstocked_stations)
            if closest_station is not None:
                overstocked_coords = (closest_station['lat'], closest_station['lng'])
                try:
                    shortest_path = nx.shortest_path(G, source=ox.distance.nearest_nodes(G, current_coords[1], current_coords[0]), target=ox.distance.nearest_nodes(G, overstocked_coords[1], overstocked_coords[0]), weight='length')
                    rebalancing_routes.append({
                        'from': current_coords,
                        'to': overstocked_coords,
                        'path': shortest_path,
                        'action': 'collect',
                        'station_name': closest_station['name']
                    })
                    current_coords = overstocked_coords
                    bikes_to_collect = min(vehicle_capacity - current_bike_load, closest_station['available_bikes'])
                    current_bike_load += bikes_to_collect
                    overstocked_stations.loc[closest_station.name, 'available_bikes'] -= bikes_to_collect
                    if overstocked_stations.loc[closest_station.name, 'available_bikes'] <= closest_station['bike_stands'] * 0.7:
                        overstocked_stations.drop(closest_station.name, inplace=True)
                except nx.NetworkXNoPath:
                    continue

        elif current_bike_load > 0 and not understocked_stations.empty:
            closest_station = find_closest_station(G, current_coords, understocked_stations)
            if closest_station is not None:
                understocked_coords = (closest_station['lat'], closest_station['lng'])
                try:
                    shortest_path = nx.shortest_path(G, source=ox.distance.nearest_nodes(G, current_coords[1], current_coords[0]), target=ox.distance.nearest_nodes(G, understocked_coords[1], understocked_coords[0]), weight='length')
                    rebalancing_routes.append({
                        'from': current_coords,
                        'to': understocked_coords,
                        'path': shortest_path,
                        'action': 'drop',
                        'station_name': closest_station['name']
                    })
                    current_coords = understocked_coords
                    bikes_to_drop = min(current_bike_load, closest_station['bike_stands'] * 0.3 - closest_station['available_bikes'])
                    current_bike_load -= bikes_to_drop
                    understocked_stations.loc[closest_station.name, 'available_bikes'] += bikes_to_drop
                    if understocked_stations.loc[closest_station.name, 'available_bikes'] >= closest_station['bike_stands'] * 0.3:
                        understocked_stations.drop(closest_station.name, inplace=True)
                except nx.NetworkXNoPath:
                    continue

    return rebalancing_routes