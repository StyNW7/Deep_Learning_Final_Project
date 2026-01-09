import joblib
import pandas as pd
import numpy as np
import torch
import os
from pymongo import MongoClient, DESCENDING
from services.inference import predict_torch
from dotenv import load_dotenv
from datetime import datetime, timedelta

scalers = joblib.load("ai_models/feature_scalers.pkl")

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env")

client = MongoClient(MONGO_URI)
db = client["Gama"]
collection = db["seoul_thirteen"]

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
    REQUIRED_RECORDS = 13 * 24
    aqi = list(
        collection.find({}, {"_id": 0})
                  .sort("data.time.s", DESCENDING)
                  .limit(REQUIRED_RECORDS)
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
    # df = pd.read_csv('aqi_data.csv')
    df = get_df_data()
    if df.empty:
        raise ValueError("DataFrame is empty. Check Database connection.")

    required_stations = [101, 102, 105, 106, 107, 109, 111, 112, 113, 119, 120, 121, 122]

    if not all(station in df['Station code'].unique() for station in required_stations):
        missing = set(required_stations) - set(df['Station code'].unique())
        raise ValueError(f"Missing data for stations: {missing}")

    df['Measurement date'] = pd.to_datetime(df['Measurement date'])

    unique_times = df['Measurement date'].unique()
    print(unique_times)
    if len(unique_times) != 24:
        raise ValueError(f"Must contain exactly 24 hours of data. Found {len(unique_times)}.")

    df = df.sort_values(by=['Measurement date', 'Station code'])
    df.to_csv("aqi_data_sorted.csv", index=False, encoding="utf-8")

    df['hour'] = df['Measurement date'].dt.hour
    df['month'] = df['Measurement date'].dt.month

    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12.0)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12.0)

    feature_cols = ['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5',
                    'hour_sin', 'hour_cos', 'month_sin', 'month_cos']

    processed_features = []
    num_stations = 13

    for feat in feature_cols:
        values = df[feat].values.reshape(24, num_stations)

        val_df = pd.DataFrame(values)

        if 'sin' not in feat and 'cos' not in feat:
            if feat in scalers:
                values_norm = scalers[feat].transform(val_df.values)
            else:
                print(f"Warning: Scaler for {feat} not found. Using raw values.")
                values_norm = val_df.values
        else:
            values_norm = val_df.values
            
        processed_features.append(values_norm)

    data_block = np.stack(processed_features, axis=-1)

    input_tensor = torch.FloatTensor(data_block).unsqueeze(0)

    prediction = predict_torch(input_tensor, model)

    pm25_values = prediction[0, :, 5].numpy() 
    pm25_input_for_scaler = pm25_values.reshape(1, 13)
    pm25_actual = scalers['PM2.5'].inverse_transform(pm25_input_for_scaler)
    pm25_final = pm25_actual.flatten()

    last_time_step = df['Measurement date'].max()

    index = keep_stations.index(station_code)
    pm25_value = pm25_final[index]

    return pm25_value, last_time_step

def predict_detail(model, station_code, device='cpu'):
    # df = pd.read_csv('aqi_data.csv')
    df = get_df_data()
    if df.empty:
        raise ValueError("DataFrame is empty. Check Database connection.")

    required_stations = [101, 102, 105, 106, 107, 109, 111, 112, 113, 119, 120, 121, 122]

    if not all(station in df['Station code'].unique() for station in required_stations):
        missing = set(required_stations) - set(df['Station code'].unique())
        raise ValueError(f"Missing data for stations: {missing}")

    df['Measurement date'] = pd.to_datetime(df['Measurement date'])

    unique_times = df['Measurement date'].unique()
    print(unique_times)
    if len(unique_times) != 24:
        raise ValueError(f"Must contain exactly 24 hours of data. Found {len(unique_times)}.")

    df = df.sort_values(by=['Measurement date', 'Station code'])
    df.to_csv("aqi_data_sorted.csv", index=False, encoding="utf-8")

    df['hour'] = df['Measurement date'].dt.hour
    df['month'] = df['Measurement date'].dt.month

    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12.0)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12.0)

    feature_cols = ['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5',
                    'hour_sin', 'hour_cos', 'month_sin', 'month_cos']

    processed_features = []
    num_stations = 13

    for feat in feature_cols:
        values = df[feat].values.reshape(24, num_stations)

        val_df = pd.DataFrame(values)

        if 'sin' not in feat and 'cos' not in feat:
            if feat in scalers:
                values_norm = scalers[feat].transform(val_df.values)
            else:
                print(f"Warning: Scaler for {feat} not found. Using raw values.")
                values_norm = val_df.values
        else:
            values_norm = val_df.values
            
        processed_features.append(values_norm)

    data_block = np.stack(processed_features, axis=-1)

    input_tensor = torch.FloatTensor(data_block).unsqueeze(0)

    prediction = predict_torch(input_tensor, model)

    feature_idx = {
        'NO2': 0,
        'O3': 1,
        'CO': 2,
        'SO2': 3,
        'PM2.5': 5
    }

    results = {}
    index = keep_stations.index(station_code)
    max_val = 0
    dominant_pollutant=""
    for pollutant, idx in feature_idx.items():
        values = prediction[0, :, idx].numpy()
        values_2d = values.reshape(1, 13)
        actual = scalers[pollutant].inverse_transform(values_2d)
        res = actual.flatten()
        if res[index] > max_val and pollutant != 'PM2.5':
            max_val = res[index]
            dominant_pollutant = pollutant
        results[pollutant] = res[index]

    last_time_step = df['Measurement date'].max()

    return results['NO2'], results['O3'], results['CO'], results['SO2'], results['PM2.5'], dominant_pollutant, last_time_step

def predict_multistep(model, device='cpu', steps=6):
    input_df = pd.read_csv('aqi_data.csv')
    input_df['Measurement date'] = pd.to_datetime(input_df['Measurement date'])

    keep_stations = [101, 102, 105, 106, 107, 109, 111, 112, 113, 119, 120, 121, 122]
    input_df = input_df[input_df['Station code'].isin(keep_stations)]

    timestamps = np.sort(input_df['Measurement date'].unique())
    if len(timestamps) < 24:
        raise ValueError(f"CSV only has {len(timestamps)} hours. Model requires 24h.")

    last_24_hours = timestamps[-24:]
    input_df = input_df[input_df['Measurement date'].isin(last_24_hours)]
    
    last_known_time = pd.to_datetime(last_24_hours[-1])

    time_df = pd.DataFrame({'Measurement date': last_24_hours})
    time_df['hour'] = time_df['Measurement date'].dt.hour
    time_df['month'] = time_df['Measurement date'].dt.month

    time_feats = {}
    time_feats['hour_sin'] = np.sin(2 * np.pi * time_df['hour'] / 24.0).values
    time_feats['hour_cos'] = np.cos(2 * np.pi * time_df['hour'] / 24.0).values
    time_feats['month_sin'] = np.sin(2 * np.pi * time_df['month'] / 12.0).values
    time_feats['month_cos'] = np.cos(2 * np.pi * time_df['month'] / 12.0).values

    feature_cols = ['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5']
    time_cols = ['hour_sin', 'hour_cos', 'month_sin', 'month_cos']

    processed_features = []

    for feat in feature_cols:
        pivot = input_df.pivot_table(index='Measurement date', columns='Station code', values=feat)
        pivot = pivot.reindex(columns=keep_stations)
        pivot = pivot.interpolate(method='linear', limit_direction='both').bfill().ffill()
        values = pivot.values
        if feat in scalers:
            values_norm = scalers[feat].transform(values)
        else:
            values_norm = values
        processed_features.append(values_norm)

    num_stations = len(keep_stations)
    for t_col in time_cols:
        t_val = time_feats[t_col].reshape(-1, 1)
        t_block = np.tile(t_val, (1, num_stations))
        processed_features.append(t_block)

    input_seq = np.stack(processed_features, axis=-1)
    current_input = torch.FloatTensor(input_seq).unsqueeze(0).to(device)

    model.eval()
    predictions_storage = []

    with torch.no_grad():
        for step in range(1, steps + 1):
            prediction = model(current_input) 
            predictions_storage.append(prediction)

            if step < steps:
                next_time = last_known_time + pd.Timedelta(hours=step)
                
                next_h = next_time.hour
                next_m = next_time.month
                
                next_time_feats = [
                    np.sin(2 * np.pi * next_h / 24.0),
                    np.cos(2 * np.pi * next_h / 24.0),
                    np.sin(2 * np.pi * next_m / 12.0),
                    np.cos(2 * np.pi * next_m / 12.0)
                ]
                
                next_time_tensor = torch.FloatTensor(next_time_feats).view(1, 1, 1, 4).to(device)
                next_time_tensor = next_time_tensor.repeat(1, 1, num_stations, 1)

                pred_unsqueezed = prediction.unsqueeze(1)
                
                new_row = torch.cat([pred_unsqueezed, next_time_tensor], dim=-1)

                current_input = torch.cat([current_input[:, 1:, :, :], new_row], dim=1)

    results_dict = {'Station Code': keep_stations}

    for step_idx, raw_pred in enumerate(predictions_storage):
        hour_label = f"{step_idx + 1}hr"
        
        for i, feat_name in enumerate(feature_cols):
            pred_norm = raw_pred[0, :, i].cpu().numpy().reshape(1, -1)

            if feat_name in scalers:
                pred_actual = scalers[feat_name].inverse_transform(pred_norm)
            else:
                pred_actual = pred_norm

            pred_actual = np.clip(pred_actual, a_min=0.0, a_max=None)
            
            col_name = f'Predicted {feat_name} ({hour_label})'
            results_dict[col_name] = pred_actual.flatten()

    results = pd.DataFrame(results_dict)
    
    return results

def get_pm25_for_station(results_df, station_code):
    station_row = results_df[results_df['Station Code'] == station_code]
    
    if station_row.empty:
        return f"Station {station_code} not found."
    
    pm25_values = [
        ("1hr", station_row['Predicted PM2.5 (1hr)'].values[0]),
        ("2hr", station_row['Predicted PM2.5 (2hr)'].values[0]),
        ("3hr", station_row['Predicted PM2.5 (3hr)'].values[0]),
        ("4hr", station_row['Predicted PM2.5 (4hr)'].values[0]),
        ("5hr", station_row['Predicted PM2.5 (5hr)'].values[0]),
        ("6hr", station_row['Predicted PM2.5 (6hr)'].values[0]),
    ]
    
    now = datetime.now()
    hourly_forecast = []
    for i, (label, pm25) in enumerate(pm25_values, start=1):
        forecast_time = now + timedelta(hours=i)
        hourly_forecast.append({
            "time": forecast_time.strftime("%Y-%m-%d %H:%M"),
            "hour24": forecast_time.strftime("%H:%M"),
            "pm25": round(float(pm25), 2)
        })
    
    return hourly_forecast