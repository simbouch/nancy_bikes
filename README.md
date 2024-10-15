# Bike Station Rebalancing App for Nancy

## Overview

This project is a Streamlit-based web application designed to help manage the bike stations in Nancy, France. It offers real-time visualization of the bike stations, highlighting those that are overstocked or understocked, and provides an optimized route for rebalancing bikes between stations. 

<img src="https://raw.githubusercontent.com/simbouch/nancy_bikes/refs/heads/main/screenshot.png" width="850"/>

## Features

- **Interactive Map**: Displays the locations of all bike stations in Nancy, along with their current status (balanced, overstocked, understocked).
- **Driver Location**: Allows the driver to input their current position and view it on the map.
- **Vehicle Parameters**: Set the vehicle's capacity and the current number of bikes.
- **Route Optimization**: Calculates the best route for collecting or depositing bikes to achieve balance across the stations.
- **Real-time Data**: Pulls live data from the JCDecaux API to keep the map updated.

## How It Works

1. **Data Loading**:
   - The app fetches live data about bike stations in Nancy from the JCDecaux API using the function `get_bike_station_data` in `call_api.py`. This data includes the number of available bikes, empty stands, and the station's coordinates.
   - The data is processed in `load_bike_station.py` and returned as a Pandas DataFrame.

2. **Classification of Bike Stations**:
   - The stations are classified as either **overstocked** (too many bikes), **understocked** (too few bikes), or **balanced**. This is done in `balance_analysis.py` using the available bike data and station capacity.

3. **Map Creation**:
   - A map centered on Nancy is created using Folium in `map_utils.py`. 
   - Bike stations are added to the map with color-coded markers based on their classification: red for overstocked, green for understocked, and blue for balanced.

4. **Driver Location**:
   - The user inputs their current location, either by manually entering latitude and longitude, or by using the default location (Nancy, France). The driver's position is then displayed on the map.

5. **Route Optimization**:
   - The app uses OSMnx to create a road network of Nancy (`create_nancy_graph` in `route_optimizer.py`).
   - Based on the driver’s location and the station data, the app calculates the best station to collect or deposit bikes to achieve balance. This is done using the function `find_best_station`, which finds the shortest path to the optimal station using NetworkX.

6. **Display and Interaction**:
   - The calculated route is displayed on the map, and a tooltip provides details such as the distance to the station and the number of bikes to collect or deposit.
   - Users can update their location, vehicle parameters, and refresh the data in real-time, ensuring up-to-date information.

## Project Structure

```
.
├── src
│   ├── __init__.py
│   ├── balance_analysis.py
│   ├── call_api.py
│   ├── load_bike_station.py
│   ├── map_utils.py
│   └── route_optimizer.py
├── main.py
├── stan.jpg
├── requirements.txt
```

### Folder and File Descriptions

- **src**: Contains all the utility scripts for data loading, analysis, and map creation.
  - `balance_analysis.py`: Classifies the bike stations based on their current balance (overstocked, understocked, or balanced).
  - `call_api.py`: Fetches live data from the JCDecaux API.
  - `load_bike_station.py`: Handles loading and preprocessing of bike station data.
  - `map_utils.py`: Contains functions for creating the map, adding stations and driver positions, and displaying optimized routes.
  - `route_optimizer.py`: Optimizes the route for bike rebalancing between stations.
- **main.py**: The main application script, built using Streamlit. It provides the user interface for interacting with the app, loading data, displaying maps, and calculating routes.
- **stan.jpg**: A sample image used in the project (optional or illustrative).
- **requirements.txt**: Lists the dependencies required for running the project.

## How to Run

1. **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <project-directory>
    ```

2. **Install dependencies**:
    Make sure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    streamlit run main.py
    ```

4. **Interact with the app**:
    - Enter your vehicle's current capacity and load.
    - Choose whether to collect or deposit bikes.
    - View the optimized route on the map.

## API Integration

The app fetches live data from the JCDecaux bike station API using the contract name `nancy`. Make sure to add your own API key in the `load_bike_station.py` file for the data fetching to work correctly.

## Requirements

- Python 3.x
- Streamlit
- Pandas
- Geopy
- Folium
- OSMnx
- NetworkX

For a full list of dependencies, refer to the `requirements.txt` file.

## License

This project is open-source and free to use.