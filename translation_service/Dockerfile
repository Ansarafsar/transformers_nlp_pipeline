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
COPY app.py .
COPY translation.py .
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5001", "--timeout", "120", "app:app"]
