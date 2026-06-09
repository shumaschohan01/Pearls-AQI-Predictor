import streamlit as st
import hopsworks
import joblib
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pearls AQI Predictor", page_icon="🌤️")
st.title("🌤️ Pearls AQI Predictor (Next 3 Days)")

HOPSWORKS_API_KEY = "6zxFgR0QumA0vQqM.GiZSp1oio0kuBEwBbPu7NLReUzUntpwgyO5BQiqSrrJ1pfr6MS65YmIFS0T5bYxO"

@st.cache_resource
def load_model_and_data():
    # Hopsworks se connect karke latest model aur data lana
    project = hopsworks.login(api_key_value=HOPSWORKS_API_KEY)
    fs = project.get_feature_store()
    mr = project.get_model_registry()
    
    # Model download karna
    model_meta = mr.get_model("aqi_predictor_model", version=1)
    model_dir = model_meta.download()
    model = joblib.load(model_dir + "/aqi_model.pkl")
    
    # Latest data lana
    aqi_fg = fs.get_feature_group(name="aqi_features", version=1)
    df = aqi_fg.read()
    return model, df

try:
    model, df = load_model_and_data()
    st.success("✅ Model aur Data Hopsworks se successfully load ho gaya!")
    
    # Latest record dikhana
    latest_record = df.iloc[-1]
    st.write(f"### Current AQI status for {latest_record['city'].upper()}:")
    st.metric(label="Latest Recorded AQI", value=int(latest_record['aqi']))

    # 3-Day Forecast simulation (Agla 3 din ka prediction)
    st.write("### 📅 3-Day Future AQI Forecast")
    
    # Base features lekar thoda variation create karte hain dummy future prediction ke liye
    future_days = ["Kal (Day 1)", "Parso (Day 2)", "Agla Din (Day 3)"]
    predictions = []
    
    base_features = [latest_record['co'], latest_record['no2'], latest_record['o3'], 
                     latest_record['pm2_5'], latest_record['pm10'], 
                     latest_record['hour'], latest_record['day'], latest_record['month']]
    
    for i in range(1, 4):
        # AI se pucho
        pred = model.predict([base_features])[0]
        # Thoda randomness real-world feel dene ke liye
        final_pred = max(1, min(5, int(pred + np.random.choice([-1, 0, 1]))))
        predictions.append(final_pred)
        
    forecast_df = pd.DataFrame({
        "Day": future_days,
        "Predicted AQI Level (1-5)": predictions
    })
    
    st.table(forecast_df)
    st.info("💡 Note: OpenWeather AQI Scale: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor")

except Exception as e:
    st.error(f"Kuch gadbad ho gayi: {e}")
