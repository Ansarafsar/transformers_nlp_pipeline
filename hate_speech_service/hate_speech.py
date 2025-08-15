import fasttext
import re
import emoji
from indicnlp.tokenize import indic_tokenize
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# Initialize fastText and all models
MODEL_PATH = "/app/models/lid.176.bin"
lang_detector = fasttext.load_model(MODEL_PATH)
MODEL_CONFIG = {
    "muril": "google/muril-base-cased",
    "indicbert": "ai4bharat/indic-bert",
    "xlmr": "xlm-roberta-base",
    "distilbert": "distilbert-base-multilingual-cased",
    "mbert": "bert-base-multilingual-cased"
}
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizers = {name: AutoTokenizer.from_pretrained(model) for name, model in MODEL_CONFIG.items()}
models = {name: AutoModelForSequenceClassification.from_pretrained(model).to(device)
          for name, model in MODEL_CONFIG.items()}

def detect_language(text):
    if not text or not text.strip():
        return {"language": None, "confidence": 0.0, "is_ambiguous": True}
    text = text.replace("\n", " ")
    predictions = lang_detector.predict(text, k=1)
    label = predictions[0][0].replace("__label__", "")
    confidence = predictions[1][0]
    is_ambiguous = confidence < 0.9
    return {
        "language": "mixed" if is_ambiguous else label,
        "confidence": confidence,
        "is_ambiguous": is_ambiguous
    }

def preprocess_text(text, language_info):
    if not text or not text.strip():
        return None
    language = language_info["language"]
    is_ambiguous = language_info["is_ambiguous"]
    text = re.sub(r'\s+', ' ', text.strip())
    text = emoji.demojize(text, language='en')
    if language in ['en', 'mixed'] or is_ambiguous:
        text = text.lower()
    normalizer_factory = IndicNormalizerFactory()
    if language == 'hi':
        normalizer = normalizer_factory.get_normalizer('hi')
        text = normalizer.normalize(text)
        tokens = indic_tokenize.trivial_tokenize(text, lang='hi')
        text = ' '.join(tokens)
    elif language == 'bn':
        normalizer = normalizer_factory.get_normalizer('bn')
        text = normalizer.normalize(text)
        tokens = indic_tokenize.trivial_tokenize(text, lang='bn')
        text = ' '.join(tokens)
    else:
        text = re.sub(r'[^\w\s:]+', '', text)
    return text

def rule_based_check(text, language_info):
    if not text:
        return {"score_boost": 0.0, "matched_rules": []}
    language = language_info["language"]
    is_ambiguous = language_info["is_ambiguous"]
    lexicons = {
        'en': ['idiot', 'stupid', 'useless', 'loser'],
        'hi': ['बेवकूफ', 'मूर्ख', 'बकवास', 'नालायक'],
        'bn': ['বোকা', 'মূর্খ', 'বাজে', 'অযোগ্য'],
        'mixed': ['bakwas', 'bhai', 'useless']
    }
    sarcasm_patterns = [r'\b(wow|really)\b', r'[!]{2,}', r':\w+_face:']
    matched_rules = []
    score_boost = 0.0
    lexicon = lexicons.get(language, lexicons['mixed'] if is_ambiguous else [])
    for term in lexicon:
        if term in text.lower():
            matched_rules.append(f"Slur: {term}")
            score_boost += 0.2
    for pattern in sarcasm_patterns:
        if re.search(pattern, text.lower()):
            matched_rules.append(f"Sarcasm: {pattern}")
            score_boost += 0.1
    return {"score_boost": min(score_boost, 0.5), "matched_rules": matched_rules}

def classify_text(text, model_name):
    tokenizer = tokenizers[model_name]
    model = models[model_name]
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1).detach().cpu().numpy()[0]
    return probs[1]  # Probability of hate speech

def detect_hate_speech(text, config):
    language_info = detect_language(text)
    if language_info["language"] is None:
        return {"score": 0.0, "details": {"language": None, "rules": []}}
    normalized_text = preprocess_text(text, language_info)
    if not normalized_text:
        return {"score": 0.0, "details": {"language": language_info["language"], "rules": []}}

    # Run all models
    model_scores = {}
    for model_name in MODEL_CONFIG:
        try:
            hate_prob = classify_text(normalized_text, model_name)
            model_scores[model_name] = float(hate_prob)
        except Exception as e:
            model_scores[model_name] = f"Error: {str(e)}"

    # Decision fusion
    valid_scores = [score for score in model_scores.values() if isinstance(score, float)]
    avg_score = np.mean(valid_scores) if valid_scores else 0.0
    rule_output = rule_based_check(normalized_text, language_info)
    final_score = min(avg_score + rule_output["score_boost"], 1.0) if avg_score > 0.5 else max(avg_score - rule_output["score_boost"], 0.0)

    details = {
        "language": language_info["language"],
        "rules": rule_output["matched_rules"]
    }
    return {"score": float(final_score), "details": details}
