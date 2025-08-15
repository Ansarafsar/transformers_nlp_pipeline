from flask import Flask, request, jsonify
import yaml
from translation import translate_text

app = Flask(__name__)

# Load config
with open("/app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in JSON input"}), 400
        text = data["text"].strip()
        if not text:
            return jsonify({"error": "Empty text input"}), 400
        result = translate_text(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
