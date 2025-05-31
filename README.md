# REM Waste - English Accent Analyzer

A web-based application that detects English accents from video URLs using state-of-the-art open-source tools.

## 🌐 Project Overview

The **REM Waste - English Accent Analyzer** allows users to:
- Analyze the English accent in any public video link (YouTube, Loom, direct MP4).
- Receive a predicted accent from 16 supported varieties.
- Get confidence scores powered by deep learning models from SpeechBrain.

> Useful for language learners, educators, researchers, and content creators.

---

## 🚀 Features

- 🎥 **Video Downloading**: Supports YouTube, Loom, MP4 via `yt-dlp`.
- 🔊 **Audio Extraction**: Converts video to 16kHz mono WAV using `FFmpeg`.
- 🧠 **Accent Detection**: Uses SpeechBrain’s `Jzuluaga/accent-id-commonaccent_ecapa` model.
- 🌎 **16 Accents Recognized**:
  - US, England, Australia, Indian, Canada, Bermuda, Scotland, African,
  - Ireland, New Zealand, Wales, Malaysia, Philippines, Singapore, Hong Kong, South Atlantic
- 🧾 **Confidence Scores**: Output with each prediction.
- ⚙️ **Async Tasks**: Long processes are handled via `Flask-Executor`.
- 📱 **Responsive UI**: Built with HTML and Tailwind CSS.
- ♻️ **Temporary File Cleanup**: Auto-managed for each request.

---

## 🗂️ Project Structure

```bash
rem_waste_accent_analyzer/
├── app.py                # Flask app with routes and async execution
├── video_processing.py   # Video download and audio extraction logic
├── accent_analysis.py    # Loads model and detects accent
├── templates/
│   └── index.html        # Web interface template
└── static/
    └── style.css         # Custom Tailwind styles
```

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.8+
- FFmpeg
- yt-dlp

### 2. Installation

```bash
# Clone the repository or set up the folder manually
git clone https://github.com/yourusername/rem_waste_accent_analyzer.git
cd rem_waste_accent_analyzer

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Clean install dependencies
pip uninstall speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor yt-dlp -y
pip install --upgrade speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor yt-dlp
```

### 3. Optional: Clean HuggingFace Cache
```bash
rm -rf ~/.cache/huggingface
```

---

## ▶️ Usage

```bash
# Run the application
python app.py
```

Then open: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🐳 Docker Support

Create a `Dockerfile` in the root directory:

```Dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt update && apt install -y ffmpeg &&     pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor yt-dlp

EXPOSE 5000

CMD ["python", "app.py"]
```

To build and run the container:

```bash
docker build -t accent-analyzer .
docker run -p 5000:5000 accent-analyzer
```

---

## 🔍 Troubleshooting

- **yt-dlp file write error**: Check directory permissions.
- **FFmpeg path error**: Ensure FFmpeg is installed and added to PATH.
- **SpeechBrain model error**: Clear huggingface cache if needed.
- **No result displayed**: Check browser console for JavaScript errors.

---

## 📦 Technologies

**Backend**: Flask, Flask-Executor, yt-dlp, FFmpeg, SpeechBrain, PyTorch  
**Frontend**: HTML, Tailwind CSS, JavaScript (Fetch API)

---

## 📜 License

MIT License. Use freely with attribution.
