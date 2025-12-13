from flask import Flask, request, jsonify
from flask_cors import CORS

from services.preprocessing import predict, station_code_map, predict_detail
from services.inference import get_model

app = Flask(__name__)
cors = CORS(app, origins='*')

GLOBAL_MODEL = get_model()
print("Model loaded successfully.")

#api/predict?station=Mapo-gu
@app.route("/api/predict")
def predict_pollutant():
    try:
        station = request.args.get("station")
        station_code = station_code_map[station]
        # Pass the globally loaded model
        # The result returns (numpy_array, timestamp)
        prediction, timestamp = predict(GLOBAL_MODEL, station_code)
        
        # FIX 3: Formatting for JSON response
        response = {
            "status": "success",
            "prediction": float(prediction),  # Convert numpy -> list
            "last_timestamp": str(timestamp)    # Convert pandas timestamp -> string
        }
        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500
    
#api/predict-detail?station=Mapo-gu
@app.route("/api/predict-detail")
def predict_pollutant_detail():
    try:
        station = request.args.get("station")
        station_code = station_code_map[station]
        no2_prediction, o3_prediction, co_prediction, so2_prediction, pm25_prediction, dominant_pollutant, timestamp = predict_detail(GLOBAL_MODEL, station_code)
        
        response = {
            "status": "success",
            "no2_prediction": float(no2_prediction),
            "o3_prediction": float(o3_prediction),
            "co_prediction": float(co_prediction),
            "so2_prediction": float(so2_prediction),
            "pm25_prediction": float(pm25_prediction),
            "dominant_pollutant": str(dominant_pollutant),
            "last_timestamp": str(timestamp)
        }
        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)