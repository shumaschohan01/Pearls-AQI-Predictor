import streamlit as st
import joblib
import pandas as pd

st.title("Pearls AQI Predictor")
model = joblib.load('model.pkl')

hour = st.slider("Select Hour", 0, 23, 12)
if st.button("Predict"):
    prediction = model.predict([[hour]])
    st.write(f"Predicted AQI for hour {hour}: {prediction[0]:.2f}")
