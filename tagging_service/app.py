from flask import Flask, request, jsonify
import yaml
from tagging import generate_tags

app = Flask(__name__)

# Load config
with open("/app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

@app.route("/tag", methods=["POST"])
def tag_text():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in JSON input"}), 400
        text = data["text"].strip()
        if not text:
            return jsonify({"error": "Empty text input"}), 400
        tags = generate_tags(text, config["tagging"])
        return jsonify({"tags": tags})
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
