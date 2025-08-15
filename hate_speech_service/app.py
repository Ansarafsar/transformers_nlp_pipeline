from flask import Flask, request, jsonify
import yaml
from hate_speech import detect_hate_speech

app = Flask(__name__)

# Load config
with open("/app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

@app.route("/detect", methods=["POST"])
def detect():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in JSON input"}), 400
        text = data["text"].strip()
        if not text:
            return jsonify({"error": "Empty text input"}), 400
        result = detect_hate_speech(text, config["hate_speech"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
