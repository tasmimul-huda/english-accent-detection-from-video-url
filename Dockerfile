# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

COPY . /app

RUN apt update && apt install -y ffmpeg && \
    pip install --no-cache-dir --upgrade pip && \
    # pip install --no-cache-dir speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor yt-dlp
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
