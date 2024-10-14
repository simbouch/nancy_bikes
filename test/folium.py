import folium

# Coordonnées géographiques de Nancy
nancy_coords = [48.692054, 6.184417]

# Créer une carte centrée sur Nancy
mymap = folium.Map(location=nancy_coords, zoom_start=13)

# Afficher la carte
mymap