import torch
from easynmt import EasyNMT
from langdetect import detect_langs

# Check for GPU support
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[TranslationService] Using device: {device}")

# Load model once at service start
model = EasyNMT("m2m_100_418M", device=device)

def translate_text(input_text: str) -> dict:
    try:
        if not input_text or not input_text.strip():
            return {"error": "Empty text input."}

        text = input_text.strip()

        # Detect language
        langs = detect_langs(text)
        detected_lang = langs[0].lang if langs else "unknown"
        confidence = langs[0].prob if langs else 0.0

        # Translate
        translated_text = model.translate(text, target_lang="en", beam_size=5)

        return {
            "lang": detected_lang.lower(),
            "confidence": round(confidence, 4),
            "translated_text": translated_text
        }

    except Exception as e:
        return {"error": f"Translation error: {str(e)}"}
