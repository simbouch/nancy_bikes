
# 🚴‍♂️ Nancy Bike Rebalancing App 🚴‍♀️

## Project Overview

The **Nancy Bike Rebalancing App** is an interactive tool developed with Streamlit to optimize the redistribution of bikes across various bike stations in Nancy, France. It helps users determine the best station to either collect or deposit bikes, ensuring an efficient rebalancing process.

## Scoring System

The scoring system is a key part of the application. It helps to determine the most optimal station for rebalancing based on:

1. **Distance**: Stations closer to the user's location are prioritized.
2. **Availability**:
   - **For collecting**: Stations with more available bikes score higher.
   - **For depositing**: Stations with more available bike stands score higher.

### Scoring Formula

- **Collecting Bikes**:
  \[
  	ext{{score}} = rac{{	ext{{available\_bikes}}}}{{	ext{{distance}} + 1}}
  \]

- **Depositing Bikes**:
  \[
  	ext{{score}} = rac{{	ext{{available\_bike\_stands}}}}{{	ext{{distance}} + 1}}
  \]

This formula ensures that stations with more bikes or available stands and closer proximity get a higher score, leading to more efficient rebalancing.

## App Functionality

1. **View Bike Stations on a Map**: All bike stations in Nancy are displayed on an interactive map, with color-coded markers indicating their status (overstocked, understocked, balanced).
2. **Enter Location**: Users can either manually enter their location or use automated geolocation.
3. **Choose Action**: The user selects whether they want to **collect** bikes from overstocked stations or **deposit** bikes into understocked stations.
4. **Calculate Optimal Route**: The app calculates and displays the best station based on the scoring system.
5. **Rebalancing**: After the station is selected, the app provides information on how many bikes to collect or deposit.

## Secrets Management

The app uses a `secrets.toml` file to securely store API keys for accessing the JCDecaux bike station data. This file is located in the `.streamlit` directory and is not tracked by version control (it is added to `.gitignore`).

### Configuration of `secrets.toml`

Create a `.streamlit/secrets.toml` file with the following content:

```toml
[secrets]
JCDECAUX_API_KEY = "your_actual_api_key"
```

The API key is accessed securely in the code via `st.secrets["JCDECAUX_API_KEY"]`.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/nancy_bikes.git
   cd nancy_bikes
   ```

2. **Install the Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Your API Key**:
   Create a `.streamlit/secrets.toml` file as described above and add your JCDecaux API key.

4. **Run the App**:
   Start the Streamlit app by running:
   ```bash
   streamlit run main.py
   ```

## Conclusion

The Nancy Bike Rebalancing App provides an efficient way to balance bike stations in the city of Nancy. Using the scoring system, users are directed to the most suitable station for collecting or depositing bikes, ensuring smoother operations and improved availability for all users.

