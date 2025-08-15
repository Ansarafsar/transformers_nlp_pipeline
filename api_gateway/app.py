from flask import Flask, request, jsonify
import requests
import yaml

app = Flask(__name__)

# Load config
with open("/app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

HATE_SPEECH_THRESHOLD = config["hate_speech"]["threshold"]

@app.route("/process", methods=["POST"])
def process_text():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in JSON input"}), 400
        text = data["text"].strip()
        if not text:
            return jsonify({"error": "Empty text input"}), 400

        # Call translation service
        translation_response = requests.post(
            "http://translation_service:5001/translate",
            json={"text": text},
            timeout=10
        )
        translation_response.raise_for_status()
        translation_result = translation_response.json()
        if "error" in translation_result:
            return jsonify(translation_result), 500
        translated_text = translation_result["translated_text"]
        lang = translation_result["lang"]
        confidence = translation_result["confidence"]

        # Call hate speech service
        hate_speech_response = requests.post(
            "http://hate_speech_service:5002/detect",
            json={"text": translated_text},
            timeout=10
        )
        hate_speech_response.raise_for_status()
        hate_speech_result = hate_speech_response.json()
        if "error" in hate_speech_result:
            return jsonify(hate_speech_result), 500
        hate_speech_score = hate_speech_result["score"]
        hate_speech_details = hate_speech_result["details"]

        # Call tagging service
        tagging_response = requests.post(
            "http://tagging_service:5003/tag",
            json={"text": translated_text},
            timeout=10
        )
        tagging_response.raise_for_status()
        tagging_result = tagging_response.json()
        if "error" in tagging_result:
            return jsonify(tagging_result), 500
        tags = tagging_result["tags"]

        # Log result
        log_data = {
            "original_text": text,
            "translated_text": translated_text,
            "language": lang,
            "confidence": confidence,
            "hate_speech_score": hate_speech_score,
            "hate_speech_details": hate_speech_details,
            "tags": tags
        }
        log_response = requests.post(
            "http://logging_service:5004/log",
            json=log_data,
            timeout=5
        )

        # Check if flagged
        if hate_speech_score >= HATE_SPEECH_THRESHOLD:
            log_data["flagged"] = True
            log_flagged_response = requests.post(
                "http://logging_service:5004/log_flagged",
                json=log_data,
                timeout=5
            )
            return jsonify({"flagged": True, "reason": "Hate speech detected"})

        return jsonify({
            "lang": lang,
            "confidence": confidence,
            "translated_text": translated_text,
            "hatespeech": hate_speech_score,
            "details": hate_speech_details,
            "tags": tags
        })

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
