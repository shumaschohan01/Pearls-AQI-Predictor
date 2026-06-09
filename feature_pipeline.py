import os
import subprocess
import sys

# Agar robot ke paas pyarrow nahi hai, toh ye line use khud install kar degi!
try:
    import pyarrow
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "pyarrow", "hopsworks==4.7.*"]
    )

import datetime
import hopsworks
import pandas as pd
import requests

# Baaki ka aapka purana code yahan se shuru hoga...
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
HOPSWORKS_API_KEY = os.environ.get("HOPSWORKS_API_KEY")
CITY = "Delhi"


def fetch_aqi_data(city, api_key):
    # Pehle city ke coordinates (lat, lon) nikalte hain
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_res = requests.get(geo_url).json()

    if not geo_res:
        print("City nahi mili!")
        return None

    lat, lon = geo_res[0]["lat"], geo_res[0]["lon"]

    # Ab real AQI data nikalte hain
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    aqi_res = requests.get(aqi_url).json()

    # Data ko ek simple format me convert karte hain
    data = aqi_res["list"][0]
    components = data["components"]

    df_dict = {
        "city": [city.lower()],
        "timestamp": [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],  # Kis time data mila
        "aqi": [data["main"]["aqi"]],  # Target variable (1 se 5 tak)
        "co": [components["co"]],
        "no2": [components["no2"]],
        "o3": [components["o3"]],
        "pm2_5": [components["pm2_5"]],
        "pm10": [components["pm10"]],
        # Time-based features (AI ko samajhne me madad milti hai)
        "hour": [datetime.datetime.now().hour],
        "day": [datetime.datetime.now().day],
        "month": [datetime.datetime.now().month],
    }

    return pd.DataFrame(df_dict)


# --- MAIN EXECUTION ---
print("🚀 Data fetch ho raha hai...")
df = fetch_aqi_data(CITY, OPENWEATHER_API_KEY)

if df is not None:
    print("📦 Hopsworks Locker (Feature Store) se connect ho rahe hain...")
    project = hopsworks.login(api_key_value=HOPSWORKS_API_KEY)
    fs = project.get_feature_store()

    # Digital locker me ek drawer (Feature Group) banana
    aqi_fg = fs.get_or_create_feature_group(
        name="aqi_features",
        version=1,
        primary_key=["city", "timestamp"],
        description="Air Quality Index features including pollutants and time data",
    )

    # Data ko drawer me save karna
    aqi_fg.insert(df)
    print("✅ Data successfully locker me save ho gaya!")
