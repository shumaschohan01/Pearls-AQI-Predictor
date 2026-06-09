import requests
import pandas as pd
from datetime import datetime
import os

# Use the environment variable instead of hardcoding the key
API_KEY = os.getenv("API_KEY")
LAT, LON = 24.8607, 67.0011
CSV_FILE = "aqi_data.csv"

def fetch_and_save():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['list'][0]
        record = {
            "timestamp": datetime.now(),
            "aqi": data['main']['aqi'],
            "pm2_5": data['components']['pm2_5']
        }
        df = pd.DataFrame([record])
        # Append to CSV
        df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
        print("Data captured successfully.")
    else:
        print("API Error:", response.status_code)

if __name__ == "__main__":
    fetch_and_save()
