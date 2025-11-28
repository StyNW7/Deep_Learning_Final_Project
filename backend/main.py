from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

# try:
#     model = load_model('./covid19_resnet.keras')
#     print("COVID model loaded successfully.")
# except Exception as e:
#     print(f"Error loading COVID model: {e}")
#     raise e

# model_classification = joblib.load('knn_model.pkl')

@app.route('/api/test', methods=['GET'])
def users():
    return jsonify(
        {
            "users": [
                'ricky',
                'nathan',
                'rich'
            ]
        }
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)