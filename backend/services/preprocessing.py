import joblib
import pandas as pd
import numpy as np
import torch
import os
from pymongo import MongoClient, DESCENDING
from services.inference import predict_torch
from dotenv import load_dotenv

scalers = joblib.load("ai_models/seoul_scalers_spta.pkl")

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env")

client = MongoClient(MONGO_URI)
db = client["Gama"]           # database name
collection = db["seoul_thirteen"]      # collection name

station_code_map = {
    "Jongno-gu": 101,
    "Jung-gu": 102,
    "Seodaemun-gu": 105,
    "Mapo-gu": 106,
    "Seongdong-gu": 107,
    "Dongdaemun-gu": 109,
    "Seongbuk-gu": 111,
    "Gangbuk-gu": 112,
    "Dobong-gu": 113,
    "Yeongdeungpo-gu": 119,
    "Dongjak-gu": 120,
    "Gwanak-gu": 121,
    "Seocho-gu": 122,
}

keep_stations = [101, 102, 105, 106, 107, 109, 111, 112, 113, 119, 120, 121, 122]

def get_df_data():
    #no need to sort
    #but need to convert to station code
    #check that there must be 24 unique timestamps
    #ensure all stations are present
    #just get to the first comma

    #prepare adjacency matrix
    #and scalers
    #and model
    #preprocess date to sin and cos
    REQUIRED_RECORDS = 13 * 24
    aqi = list(
        collection.find({}, {"_id": 0})
                  .sort("data.time.s", DESCENDING) # sort by time (newest first)
                  .limit(REQUIRED_RECORDS) #later change to 13 * 24 = 312
    )
    if not aqi:
        raise ValueError("No data found in MongoDB collection 'seoul_thirteen'")
    
    result = []
    for doc in aqi:
        row = {}
        try:
            
            city = doc['data']['city']['name']
            city_name = city.split(",")[0]

            if city_name not in station_code_map:
                print('city name not in station code')

            row['Station code'] = station_code_map[city_name]
            row['Measurement date'] = doc['data']['time']['s']
            row['NO2'] = doc['data']['iaqi']['no2']['v']
            row['O3'] = doc['data']['iaqi']['o3']['v']
            row['CO'] = doc['data']['iaqi']['co']['v']
            row['SO2'] = doc['data']['iaqi']['so2']['v']
            row['PM10'] = doc['data']['iaqi']['pm10']['v']
            row['PM2.5'] = doc['data']['iaqi']['pm25']['v']
            result.append(row)
        except KeyError as e:
            print(f"Skipping malformed document: {e}")
            continue
    
    df = pd.DataFrame(result)
    # df.to_csv("aqi_data.csv", index=False, encoding="utf-8")

    return df

def predict(model, station_code, device='cpu'):
    """
    Reads a CSV containing exactly 312 rows (24 hours * 13 stations).
    columns: Measurement date, Station code, SO2, NO2, O3, CO, PM10, PM2.5
    """

    df = get_df_data()
    if df.empty:
        raise ValueError("DataFrame is empty. Check Database connection.")

    # 2. Validation
    required_stations = [101, 102, 105, 106, 107, 109, 111, 112, 113, 119, 120, 121, 122]

    # Ensure all stations are present
    if not all(station in df['Station code'].unique() for station in required_stations):
        missing = set(required_stations) - set(df['Station code'].unique())
        raise ValueError(f"Missing data for stations: {missing}")

    # Ensure datetime format
    df['Measurement date'] = pd.to_datetime(df['Measurement date'])

    # Ensure we have exactly 24 unique timestamps
    unique_times = df['Measurement date'].unique()
    # print(unique_times)
    if len(unique_times) != 24:
        raise ValueError(f"Must contain exactly 24 hours of data. Found {len(unique_times)}.")

    # 3. CRITICAL: Sort Data
    # Must match the training order: Sort by Date, then by Station
    df = df.sort_values(by=['Measurement date', 'Station code'])
    df.to_csv("aqi_data_sorted.csv", index=False, encoding="utf-8")

    # 4. Generate Time Features (Sin/Cos)
    df['hour'] = df['Measurement date'].dt.hour
    df['month'] = df['Measurement date'].dt.month

    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12.0)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12.0)

    # 5. Feature Selection & Scaling
    feature_cols = ['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5',
                    'hour_sin', 'hour_cos', 'month_sin', 'month_cos']

    processed_features = []
    num_stations = 13

    # We iterate through features exactly like in training
    for feat in feature_cols:
        # Reshape to (Time_Steps, Stations) -> (24, 13)
        values = df[feat].values.reshape(24, num_stations)

        val_df = pd.DataFrame(values)
        #val_df = val_df.interpolate(method='linear', limit_direction='both').bfill().ffill()

        # Scale
        if 'sin' not in feat and 'cos' not in feat:
            if feat in scalers:
                values_norm = scalers[feat].transform(val_df.values)
            else:
                print(f"Warning: Scaler for {feat} not found. Using raw values.")
                values_norm = val_df.values
        else:
            values_norm = val_df.values
            
        processed_features.append(values_norm)

    # 6. Stack to Tensor
    # List of (24, 13) arrays -> Stack to (24, 13, 10)
    data_block = np.stack(processed_features, axis=-1)

    # Add Batch Dimension -> (1, 24, 13, 10)
    input_tensor = torch.FloatTensor(data_block).unsqueeze(0)

    #maybe use inference.py
    # 7. Predict
    prediction = predict_torch(input_tensor, model)

    # 8. Inverse Transform Result
    pm25_values = prediction[0, :, 5].numpy() 
    pm25_input_for_scaler = pm25_values.reshape(1, 13)
    pm25_actual = scalers['PM2.5'].inverse_transform(pm25_input_for_scaler)
    pm25_final = pm25_actual.flatten()

    last_time_step = df['Measurement date'].max()

    index = keep_stations.index(station_code)
    pm25_value = pm25_final[index]

    return pm25_value, last_time_step