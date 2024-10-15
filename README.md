
# 🚴‍♂️ Nancy Bike Rebalancing App 🚴‍♀️

## Explanation of the Scoring System and App Functionality

### **Scoring System**

The scoring system in the **Nancy Bike Rebalancing App** helps determine the best station for **collecting** or **depositing** bikes. The scoring is based on two key factors:

1. **Distance**: Stations closer to the user's location are prioritized.
2. **Availability**:
   - **Collecting**: Stations with more available bikes score higher.
   - **Depositing**: Stations with more free bike stands receive higher scores.

### **How the Scoring Works**

- For **collecting** bikes, the score is calculated using the formula:
  \[
  	ext{{score}} = rac{{	ext{{available\_bikes}}}}{{	ext{{distance}} + 1}}
  \]
- For **depositing** bikes, the score is:
  \[
  	ext{{score}} = rac{{	ext{{available\_bike\_stands}}}}{{	ext{{distance}} + 1}}
  \]

Stations with higher availability and closer proximity will receive better scores, making them the ideal choice for rebalancing.

### **App Functionality**

1. **View Bike Stations on a Map**: The app displays all bike stations in Nancy with color-coded markers showing their status.
2. **Enter Location**: Users can manually enter their current location or let the app automatically detect it.
3. **Select Action**: Choose between **collecting** bikes from overstocked stations or **depositing** into understocked stations.
4. **Calculate Optimal Route**: The app calculates and shows the optimal route to the best station based on the scoring system.
5. **Rebalance Bikes**: The app provides the number of bikes to collect or deposit, ensuring stations are efficiently balanced.

### **Secrets Management (secrets.toml)**

The API key is securely stored in a `secrets.toml` file located in the `.streamlit` directory. This file is not tracked by version control and should be added to `.gitignore`.

To configure the API key, create the following structure:
```
.streamlit/secrets.toml
```
With the content:
```toml
[secrets]
JCDECAUX_API_KEY = "your_actual_api_key"
```

This ensures that the sensitive information is securely managed.
