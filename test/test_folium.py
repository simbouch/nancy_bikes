import folium
import json

# Load the JSON data from the file
with open('./Src/nancy.json', 'r', encoding='utf-8') as file:
    stations_data = json.load(file)

# Coordinates of Nancy
nancy_coords = [48.692054, 6.184417]

# Create a map centered on Nancy
mymap = folium.Map(location=nancy_coords, zoom_start=13)

# Add a marker for each bike station
for station in stations_data:
    # Extract data for each station
    name = station['name']
    latitude = station['latitude']
    longitude = station['longitude']
    address = station['address']
    
    # Create a popup with station information
    popup_text = f"{name}<br>{address}"
    
    # Add marker to the map
    folium.Marker(
        location=[latitude, longitude],
        popup=popup_text,
        tooltip=name  # Tooltip shows station name on hover
    ).add_to(mymap)

# Save the map to an HTML file
map_filename = "nancy_bike_stations.html"
mymap.save(map_filename)

# Inject JavaScript to reload the page every 30 seconds
with open(map_filename, 'a') as f:
    f.write("""
    <script>
        setTimeout(function(){
           window.location.reload(1);
        }, 30000);  // Reload every 30 seconds
    </script>
    """)

print(f"Map with bike stations saved! Open '{map_filename}' to view it.")
