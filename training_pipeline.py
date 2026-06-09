import joblib
import hopsworks
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

HOPSWORKS_API_KEY = "6zxFgR0QumA0vQqM.GiZSp1oio0kuBEwBbPu7NLReUzUntpwgyO5BQiqSrrJ1pfr6MS65YmIFS0T5bYxO"

# 1. Locker se connect karo
project = hopsworks.login(api_key_value=HOPSWORKS_API_KEY)
fs = project.get_feature_store()

# 2. Drawer se sara data nikal lo
aqi_fg = fs.get_feature_group(name="aqi_features", version=1)
df = aqi_fg.read()

if len(df) < 5:
    print("⚠️ Data bohot kam hai! Kam se kam 5-10 rows hone do tabhi AI seekh payega.")
else:
    # 3. X (Sawaal) aur Y (Jawaab) alag karo
    # Hum pollutants aur time dekh kar AQI predict karna chahte hain
    X = df[['co', 'no2', 'o3', 'pm2_5', 'pm10', 'hour', 'day', 'month']]
    y = df['aqi']

    # Test aur Train me baanto (80% seekhne ke liye, 20% test ke liye)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. AI Model (Random Forest) ko train karo
    print("🧠 AI Model seekh raha hai...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Check karo AI kitna hoshiyar bana
    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    print(f"📊 Model Error (RMSE): {rmse} (Jitna kam ho utna accha)")

    # 6. Model ko computer me save karo
    model_path = "aqi_model.pkl"
    joblib.dump(model, model_path)
    print("💾 Model local save ho gaya.")

    # 7. Model ko Hopsworks ke Model Registry (AI ki Almari) me daal do
    mr = project.get_model_registry()
    hopsworks_model = mr.python.create_model(
        name="aqi_predictor_model",
        metrics={"RMSE": rmse},
        description="Random Forest Regressor to predict AQI"
    )
    hopsworks_model.save(model_path)
    print("🚀 Model Hopsworks Model Registry me upload ho gaya!")
