# syntax=docker/dockerfile:1
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge && \
    rm -rf /tmp/*
COPY app.py .
COPY logger.py .
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5004", "--timeout", "120", "app:app"]
