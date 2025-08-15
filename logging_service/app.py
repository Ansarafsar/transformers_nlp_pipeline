from flask import Flask, request, jsonify
import yaml
from logger import log_input

app = Flask(__name__)

# Load config
with open("/app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

@app.route("/log", methods=["POST"])
def log_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        log_input(data, config)
        return jsonify({"status": "Logged successfully"})
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
