import requests
import pandas as pd
import joblib

# -----------------------------
# CONFIGURATION
# -----------------------------
BASE_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

MODEL_PATH = "/Users/assolabasova/Desktop/SPUR 2025/BlairK /cooling_decision_model.pkl"

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

# -----------------------------
# FUNCTIONS
# -----------------------------

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
        raise ValueError("❌ Failed to fetch data from NASA POWER API.")

    df = pd.DataFrame(data["properties"]["parameter"])
    df = df.rename(columns={"T2M": "Temperature", "ALLSKY_SFC_SW_DWN": "Irradiance"})
    df["Hour"] = range(len(df))

    if hour not in df["Hour"].values:
        raise ValueError("❌ Hour out of range for data (0–23).")

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
    return panel_temp, energy_gain, cooling_cost, should_cool


def predict_from_model(T_amb, G, hour):
    """Load trained model and predict output, aligned with training features."""
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("⚠️ Model file not found. Skipping prediction.")
        return None

    panel_temp = T_amb + ((NOCT - 20) / 800) * G

    features_dict = {
        "AmbientTemp_C": T_amb,
        "Irradiance_Wm2": G,
        "hour": hour,
        "panel_temp": panel_temp
    }

    feature_order = model.feature_names_in_
    features_aligned = pd.DataFrame([[features_dict[f] for f in feature_order]], columns=feature_order)

    return model.predict(features_aligned)[0]


# -----------------------------
# MAIN INTERFACE
# -----------------------------
def main():
    print("🌞 Solar Cooling Real-World Checker 🌡️")

    # --- Sample city and date/time ---
    place = "New York, USA"
    year, month, day, hour = 2023, 7, 15, 14  # Example: July 15, 2023 at 14:00
    coords = get_coordinates(place)
    if coords:
        lat, lon, name = coords
        print(f"✅ Using sample city: {name} (Lat: {lat:.3f}, Lon: {lon:.3f})")
    else:
        print("❌ Could not fetch coordinates for sample city.")
        return

    # --- Fetch weather data ---
    print(f"\n🌍 Fetching real weather data for {name} on {year}-{month:02d}-{day:02d} at {hour}:00...")
    try:
        real_data = fetch_weather_data(lat, lon, year, month, day, hour)
        T_amb = real_data["Temperature"]
        G = real_data["Irradiance"]
        print(f"✅ Real Weather Data: {real_data}")
    except Exception as e:
        print(str(e))
        return

    # --- Physics-based calculation ---
    panel_temp, energy_gain, cooling_cost, should_cool = physics_based_check(T_amb, G)
    print(f"\n⚙️ Physics-based calculation:")
    print(f"Panel Temperature: {panel_temp:.2f} °C")
    print(f"Energy Gain from Cooling: {energy_gain:.2f} W")
    print(f"Cooling Cost (pump): {cooling_cost:.2f} W")
    print(f"Cooling Beneficial: {'Yes' if should_cool else 'No'}")

    # --- ML model check ---
    prediction = predict_from_model(T_amb, G, hour)
    if prediction is not None:
        print(f"\n🔮 ML Model Prediction: {'Yes' if prediction else 'No'}")
        print(f"✅ Model agrees with physics: {prediction == should_cool}")
    else:
        print("\n⚠️ Could not compare since model file not found.")

    print("\n✨ All tasks completed successfully!")


if __name__ == "__main__":
    main()
