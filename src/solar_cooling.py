"""
Solar Panel Cooling Optimization Module
Contains all core logic for cooling decision analysis
"""

import requests
import pandas as pd
import joblib

# -----------------------------
# CONFIGURATION
# -----------------------------
BASE_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

# -----------------------------
# PANEL & PUMP CONSTANTS
# -----------------------------
A_panel = 0.63 * 0.45       # m²
eta_ref = 0.18              # 18%
beta = 0.005
NOCT = 45
T_threshold = 45
T_target = 35
pump_power_rated = 2
pump_efficiency = 0.85
pump_power_Wh = pump_power_rated / pump_efficiency
min_runtime = 6             # minutes


def get_coordinates(place):
    """Find latitude and longitude for any city/town using OpenStreetMap."""
    params = {"q": place, "format": "json", "limit": 1}
    response = requests.get(GEOCODE_URL, params=params, headers={"User-Agent": "solar-cooling-app"})
    data = response.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]


def fetch_weather_data(lat, lon, year, month, day, hour):
    """Fetch real hourly temperature and irradiance data from NASA POWER."""
    start = f"{year}{month:02d}{day:02d}"
    end = start

    params = {
        "latitude": lat,
        "longitude": lon,
        "community": "re",
        "parameters": "T2M,ALLSKY_SFC_SW_DWN",
        "start": start,
        "end": end,
        "format": "JSON"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "properties" not in data or "parameter" not in data["properties"]:
        raise ValueError("Failed to fetch data from NASA POWER API.")

    df = pd.DataFrame(data["properties"]["parameter"])
    df = df.rename(columns={"T2M": "Temperature", "ALLSKY_SFC_SW_DWN": "Irradiance"})
    df["Hour"] = range(len(df))

    if hour not in df["Hour"].values:
        raise ValueError("Hour out of range for data (0–23).")

    row = df[df["Hour"] == hour]
    return row[["Temperature", "Irradiance"]].iloc[0].to_dict()


def physics_based_check(T_amb, G):
    """Compute panel temp, energy gain, and whether cooling is beneficial."""
    panel_temp = T_amb + ((NOCT - 20) / 800) * G

    eta_unc = max(eta_ref * (1 - beta * (panel_temp - 25)), 0)
    P_unc = eta_unc * G * A_panel

    eta_cool = max(eta_ref * (1 - beta * (T_target - 25)), 0)
    P_cool = eta_cool * G * A_panel

    energy_gain = P_cool - P_unc
    cooling_cost = pump_power_Wh

    should_cool = energy_gain > cooling_cost
    return panel_temp, energy_gain, cooling_cost, should_cool, P_unc, P_cool


def predict_from_model(T_amb, G, hour, model_path="models/cooling_decision_model.pkl"):
    """Load trained model and predict output, aligned with training features."""
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        return None, "Model file not found"

    panel_temp = T_amb + ((NOCT - 20) / 800) * G

    features_dict = {
        "AmbientTemp_C": T_amb,
        "Irradiance_Wm2": G,
        "hour": hour,
        "panel_temp": panel_temp
    }

    feature_order = model.feature_names_in_
    features_aligned = pd.DataFrame([[features_dict[f] for f in feature_order]], columns=feature_order)

    return model.predict(features_aligned)[0], None
