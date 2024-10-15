# Bike Station Rebalancing App for Nancy

## Overview

This project is a Streamlit-based web application designed to help manage the bike stations in Nancy, France. It offers real-time visualization of the bike stations, highlighting those that are overstocked or understocked, and provides an optimized route for rebalancing bikes between stations. 

## Features

- **Interactive Map**: Displays the locations of all bike stations in Nancy, along with their current status (balanced, overstocked, understocked).
- **Driver Location**: Allows the driver to input their current position and view it on the map.
- **Vehicle Parameters**: Set the vehicle's capacity and the current number of bikes.
- **Route Optimization**: Calculates the best route for collecting or depositing bikes to achieve balance across the stations.
- **Real-time Data**: Pulls live data from the JCDecaux API to keep the map updated.

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