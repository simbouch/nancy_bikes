import folium

def create_nancy_map():
    """Creates a map centered around Nancy, France."""
    nancy_coords = [48.6844, 6.1844]
    return folium.Map(location=nancy_coords, zoom_start=13)

def add_bike_stations_to_map(stations_df, nancy_map):
    """Adds bike station markers to a Folium map based on station balance status."""
    for _, station in stations_df.iterrows():
        folium.Marker(
            location=[station['lat'], station['lng']],
            popup=f"Station: {station['name']}<br>Bikes Available: {station['available_bikes']}<br>Status: {station['balance_status']}",
            icon=folium.Icon(color='blue' if station['balance_status'] == 'balanced' else ('green' if station['balance_status'] == 'understocked' else 'red'), icon='bicycle', prefix='fa')
        ).add_to(nancy_map)
    return nancy_map
