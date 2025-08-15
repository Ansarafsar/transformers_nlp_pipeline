# syntax=docker/dockerfile:1
FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    g++-11 \
    libstdc++6 \
    apt-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 cache purge && \
    rm -rf /tmp/*
RUN wget -nc https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -P models/
COPY app.py .
COPY hate_speech.py .
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5002", "--timeout", "120", "app:app"]
