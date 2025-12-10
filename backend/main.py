from flask import Flask, request, jsonify
from flask_cors import CORS
# from pymongo import MongoClient, DESCENDING

from services.preprocessing import predict
from services.inference import get_model

app = Flask(__name__)
cors = CORS(app, origins='*')

GLOBAL_MODEL = get_model()
print("Model loaded successfully.")

# MONGO_URI = os.getenv("MONGO_URI")

# if not MONGO_URI:
#     raise ValueError("MONGO_URI not found in .env")

# client = MongoClient(MONGO_URI)
# db = client["Gama"]
# collection = db["seoul_thirteen"]

# @app.route("/api/data")
# def get_data():
#     aqi = list(
#         collection.find({}, {"_id": 0})
#                   .sort("data.time.s", DESCENDING) # sort by time (newest first)
#                   .limit(13) #later change to 13 * 24 = 312
#     )
#     result = []
#     for doc in aqi:
#         row = {}
#         # city = doc['data']['city']['name']
#         # city_name = city.split(",")[0]
#         # row['Station code'] = station_code_map[city_name]
#         row['Station code'] = doc['data']['city']['name']
#         row['Measurement date'] = doc['data']['time']['s']
#         row['NO2'] = doc['data']['iaqi']['no2']['v']
#         row['O3'] = doc['data']['iaqi']['o3']['v']
#         row['CO'] = doc['data']['iaqi']['co']['v']
#         row['SO2'] = doc['data']['iaqi']['so2']['v']
#         row['PM10'] = doc['data']['iaqi']['pm10']['v']
#         row['PM2.5'] = doc['data']['iaqi']['pm25']['v']
#         result.append(row)

#     return jsonify(result)
#api/predict?station=105
@app.route("/api/predict")
def predict_pollutant():
    try:
        station = request.args.get("station")
        station = int(station)
        # Pass the globally loaded model
        # The result returns (numpy_array, timestamp)
        prediction, timestamp = predict(GLOBAL_MODEL, station)
        
        # FIX 3: Formatting for JSON response
        response = {
            "status": "success",
            "prediction": float(prediction),  # Convert numpy -> list
            "last_timestamp": str(timestamp)    # Convert pandas timestamp -> string
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)