import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train():
    df = pd.read_csv("aqi_data.csv")
    # Simple feature engineering: Hour from timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    
    X = df[['hour']] # Simplistic example
    y = df['aqi']
    
    model = RandomForestRegressor()
    model.fit(X, y)
    joblib.dump(model, 'model.pkl')
    print("Model trained and saved.")

if __name__ == "__main__":
    train()
