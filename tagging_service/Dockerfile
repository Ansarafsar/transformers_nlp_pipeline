# syntax=docker/dockerfile:1
FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    apt-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 cache purge && \
    rm -rf /tmp/*
RUN python3 -m spacy download en_core_web_sm
COPY app.py .
COPY tagging.py .
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5003", "--timeout", "120", "app:app"]
