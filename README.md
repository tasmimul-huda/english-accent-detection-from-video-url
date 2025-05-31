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
## 🖥️ Live Demo
Try the live demo here: 
<!-- [Open in Hugging Face Spaces](https://tasmimulhuda-english-accent-detection-from-video-url.hf.space/) -->
<a href="https://tasmimulhuda-english-accent-detection-from-video-url.hf.space/" target="_blank">🚀 Live Demo</a>


🎥 Example Video URLs to Try
```
http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4
```
```
https://www.loom.com/share/20470f02b52c4d66b81f25bbfcbf5ddf?sid=f1903b0a-f996-406c-aec9-e8c65f347481
```
drive link:
https://drive.google.com/file/d/1fodg3iijiyR2Wy_TV0_ZNJlQw2aVaS7W/view?usp=sharing

https://drive.google.com/file/d/1XEcmK8mjcK_KA3wtyv3I4Eyk5sLz6H6f/view?usp=sharing
https://drive.google.com/file/d/1JTr17UssCvvq74aTEOXWh4-rXPjKml_s/view?usp=sharing

youtube:
https://www.youtube.com/watch?v=Jrjwm0O1dDY&pp=ygURYXVzdHJhbGlhbiBhY2NlbnQ%3D

### Note on Confidence Scores: 
The confidence score indicates the model's certainty in its prediction. Lower confidence scores, even with successful accent detection, are common in English accent classification. This is primarily because various English accents share a high degree of acoustic similarity, making subtle distinctions challenging for the model. The score reflects the closeness of the top probable accent candidates.
---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- FFmpeg
- yt-dlp

### 2. Installation

```bash
# Clone the repository or set up the folder manually
git clone https://github.com/tasmimul-huda/english-accent-detection-from-video-url.git
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

To build and run the container:

```bash
docker build -t accent-analyzer .
docker run -p 5000:5000 accent-analyzer
```


## 📦 Technologies

**Backend**: Flask, Flask-Executor, yt-dlp, FFmpeg, SpeechBrain, PyTorch  
**Frontend**: HTML, Tailwind CSS, JavaScript (Fetch API)

---

## 📜 License

MIT License. Use freely with attribution.
