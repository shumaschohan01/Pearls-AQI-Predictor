# 🌤️ Pearls AQI Predictor

An End-to-End MLOps Air Quality Index (AQI) Prediction System. This project automates data ingestion, feature engineering, machine learning model training, and serves live predictions through a web dashboard using a **Serverless Feature Store architecture**.

---

## 🏗️ Architecture Overview

The project follows a modular MLOps design split into three distinct pipelines:

1. **Feature Pipeline (Automation):** A GitHub Actions cron job fetches live weather/pollution data from the OpenWeather API every hour and stores it securely in the **Hopsworks Feature Store**.
2. **Training Pipeline (Machine Learning):** A Python script connects to Hopsworks, reads historical features, trains a **Random Forest Regressor** model, evaluates performance, and saves it into the **Hopsworks Model Registry**.
3. **Inference Pipeline (User Application):** A interactive **Streamlit Dashboard** that pulls the latest trained model and data from Hopsworks to provide real-time air quality metrics and a 3-day AQI forecast.

---

## 🛠️ Tech Stack & Tools

- **Language:** Python 3.10+
- **Data Source:** OpenWeather Air Pollution API
- **Feature Store & Model Registry:** [Hopsworks](https://www.hopsworks.ai/)
- **Automation / CI-CD:** GitHub Actions (Runner environment)
- **Machine Learning:** Scikit-Learn (Random Forest), Pandas, NumPy
- **Dashboard UI:** Streamlit

---

## 📂 Project Structure

```text
Pearls-AQI-Predictor/
├── .github/
│   └── workflows/
│       └── hourly_pipeline.yml  # GitHub Actions robot configuration
├── feature_pipeline.py           # Fetches API data & pushes to Hopsworks
├── training_pipeline.py          # Trains the AI model & uploads to Registry
├── app.py                        # Streamlit Web Dashboard
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
