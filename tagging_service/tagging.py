from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

MODEL_NAME = "intfloat/e5-large-v2"
sentence_model = SentenceTransformer(MODEL_NAME)
kw_model = KeyBERT(model=sentence_model)

def extract_keywords(text, top_n):
    return kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=top_n,
        use_mmr=True,
        diversity=0.7
    )

def evaluate_tag_quality(text, keywords):
    text_embedding = sentence_model.encode([text])[0]
    keyword_embeddings = sentence_model.encode([kw[0] for kw in keywords])
    similarities = cosine_similarity([text_embedding], keyword_embeddings)[0]
    return [min(max(sim, 0.0), 1.0) for sim in similarities]

def generate_tags(text, config):
    if not text or not text.strip():
        return []

    try:
        buzzwords = config.get("buzzwords", [])
        word_count = len(text.split())

        # Smart dynamic top_n calculation
        def dynamic_top_n(word_count):
            if word_count <= 10:
                return max(1, word_count // 2)
            elif word_count <= 20:
                return max(1, word_count // 3)
            elif word_count <= 30:
                return max(1, word_count // 4)
            elif word_count <= 40:
                return max(1, word_count // 5)
            elif word_count <= 50:
                return max(1, word_count // 6)
            else:
                return 20

        top_n = min(dynamic_top_n(word_count), config.get("max_keywords", 5))

        # Extract and score
        keywords = extract_keywords(text, top_n)
        scores = evaluate_tag_quality(text, keywords)
        scored_keywords = [(kw[0], kw[1] * score) for kw, score in zip(keywords, scores)]

        # Sort by confidence descending
        scored_keywords.sort(key=lambda x: x[1], reverse=True)

        # Deduplicate and filter
        unique_tags = []
        seen = set()
        for kw, _ in scored_keywords:
            kw_clean = kw.lower().strip()
            if kw_clean not in seen and kw_clean not in buzzwords:
                unique_tags.append(kw)
                seen.add(kw_clean)

        # Ensure at least one tag is returned
        if not unique_tags and scored_keywords:
            unique_tags.append(scored_keywords[0][0])

        return unique_tags

    except Exception as e:
        print(f"Tag generation error: {str(e)}")
        return []
