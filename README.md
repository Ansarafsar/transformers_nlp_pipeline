# 🧠 NO GPT - Vendor Independent Multilingual/model Hate Speech Detection and Content Curation Pipeline

A scalable, fault-tolerant microservices pipeline for detecting hate speech, translating non-English text, and generating tags for content curation on professional platforms.

> ✅ **Self-hosted** to bypass external APIs like GPT for privacy  
> ⚡ **GPU-accelerated** (sub-0.8s inference) on AWS EC2  
> 🛡️ **Open-source models** ensure data remains secure and local

---

## 🚀 Features

- **🌍 Multilingual Processing**  
  Detects and translates text in Bengali, Hindi, English, etc., using `langdetect` and `easynmt` (m2m_100_418M).

- **🚨 Hate Speech Detection**  
  Uses `fasttext` for language ID and an ensemble (MuRIL, IndicBERT, XLMR, DistilBERT, mBERT) with rule-based scoring. Flags text if score > `0.7`.

- **🏷️ Content Tagging**  
  Extracts semantic tags using `keybert` and `intfloat/e5-large-v2` for user-personalized recommendations.

- **🔄 Fault Tolerance**  
  Each module runs as a standalone service with backup models; other services stay functional even if one fails.

- **🧾 Logging & Retraining**  
  Stores flagged content in `flagged_hate_speech.jsonl` for analytics and fine-tuning.

- **🐳 Deployment**  
  Uses Docker Compose with NVIDIA GPU support, Gunicorn workers, and Nginx reverse proxy.

---

## 🎯 Use Cases

- **Professional Platforms**  
  Real-time moderation of user comments/posts on platforms like LinkedIn. Translate, flag, and tag content.

- **Privacy-Focused AI**  
  Avoids cloud APIs (like GPT), keeping all data local — ideal for enterprise or regulated environments.

- **Content Curation**  
  Tags multilingual input (e.g., _"Ami kal party te jabo" → "party plan"_) for personalization and engagement.

- **Hate Speech Monitoring**  
  Continuously retrain using logged hate speech samples in multiple languages.

- **Research & Development**  
  Modular architecture allows testing or replacing components like translators, scorers, etc.

---

## 💡 Benefits to the AI World

- **🔐 Privacy & Security**  
  Self-hosting prevents data leaks and supports GDPR-compliant workflows.

- **⚙️ Scalability**  
  Microservices scale independently — ideal for GPU-intensive production use.

- **⚡ Efficiency**  
  NVIDIA T4 GPU acceleration delivers sub-0.8s inference speed in real-time.

- **🌱 Innovation**  
  Encourages ethical AI with open models over black-box proprietary systems.

- **🌍 Sustainability**  
  Avoiding cloud inference APIs cuts cost and carbon footprint.

---

## Issues:
---
- Hey Devs, this is purely a prototype code, cloning or copying it didn't run actually untill I fix some manual fixtures and methods. 😊 If you need that please contact me ! Keys are in my hands 🗝️✌️
---
## ⚙️ Setup

### ✅ Prerequisites

- AWS EC2 `g4dn.xlarge` instance (or better)
- NVIDIA Drivers + CUDA 12.1
- Docker, Docker Compose, NVIDIA Container Toolkit
- Hugging Face Token (`HF_TOKEN`) for model downloads

---

### 🧩 Clone Repo

```bash
git clone https://github.com/<your-username>/multilingual-hate-speech-pipeline.git
cd multilingual-hate-speech-pipeline
```
## 🛠️ Environment Setup

### 🔑 Set Environment Variables

```bash
echo "HF_TOKEN=<your-huggingface-token>" > .env
```
### 🐳 Build & Run the Services
```bash
export DOCKER_BUILDKIT=1
docker-compose build
docker-compose up -d
```
- Make sure Docker, Docker Compose, and NVIDIA Container Toolkit are installed and configured.

### 🔬 Test the API Locally
```bash
curl -X POST http://localhost/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Ami kal party te jabo"}'
```
### ✅ Expected Response:
```bash
{
  "flagged": false,
  "reason": "No hate speech detected",
  "tags": ["party", "plan"]
}
```
### Postman API Testing
```
Postman: POST http://<EC2-IP>/process with {"text": "You idiot"} → {"flagged": true, "reason": "Hate speech detected"}.
```
