import json

def analyse_stations(stations_data, almost_empty, almost_full, margin_amount):
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
