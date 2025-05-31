# english-accent-detection-from-video-url

REM Waste - English Accent Analyzer
Project Overview
The REM Waste - English Accent Analyzer is a web-based application built with Flask that allows users to analyze the English accent of a speaker from a provided video URL. It leverages robust open-source tools like yt-dlp for video downloading, FFmpeg for audio extraction, and SpeechBrain for advanced English accent classification. The application is designed to be user-friendly, providing clear results and a smooth experience through a responsive web interface.

This tool is particularly useful for:

Language learners and educators to get feedback on accent.

Researchers studying speech and accents.

Content creators to understand their audience's accent distribution.

Anyone curious about the English accent in a video.

Features
Video Download: Supports downloading videos from various public platforms, including YouTube, Loom, and direct MP4 links, using yt-dlp.

Audio Extraction: Extracts high-quality audio (16kHz, mono WAV) from the downloaded video using FFmpeg.

English Accent Classification: Utilizes a pre-trained SpeechBrain model (Jzuluaga/accent-id-commonaccent_ecapa) to classify the English accent present in the audio.

Supported Accents: The model is trained to recognize 16 distinct English accents, including:

US

England

Australia

Indian

Canada

Bermuda

Scotland

African

Ireland

New Zealand

Wales

Malaysia

Philippines

Singapore

Hong Kong

South Atlantic

Confidence Score: Provides a confidence percentage for the detected accent.

Asynchronous Processing: Uses Flask-Executor to handle long-running tasks (video download, audio extraction, accent analysis) in the background, keeping the UI responsive.

Responsive UI: A clean and modern web interface built with HTML and Tailwind CSS, ensuring usability across various devices.

Temporary File Management: Automatically creates and manages temporary directories for video and audio files, with robust cleanup mechanisms.

Project Structure
rem_waste_accent_analyzer/
├── app.py                  # Main Flask application, handles routes, background tasks, and orchestrates modules.
├── video_processing.py     # Module for video downloading (yt-dlp) and audio extraction (FFmpeg).
├── accent_analysis.py      # Module for SpeechBrain model loading and accent detection logic.
├── templates/
│   └── index.html          # HTML template for the web interface.
└── static/
    └── style.css           # Custom CSS for styling the UI (uses Tailwind CSS).

Setup Instructions
Follow these steps to set up and run the application on your local machine.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+: Download from python.org.

FFmpeg: A powerful multimedia framework required for audio extraction.

Windows: Download a static build from ffmpeg.org/download.html. Extract it and add the bin directory to your system's PATH environment variable.

macOS: Install via Homebrew: brew install ffmpeg

Linux (Ubuntu/Debian): sudo apt update && sudo apt install ffmpeg

yt-dlp: A command-line program to download videos. It will be installed via pip but relies on FFmpeg.

Installation Steps
Clone the Repository (or create the project structure manually):
If you have the project files already, navigate to your project's root directory. Otherwise, create the rem_waste_accent_analyzer folder and the templates/ and static/ subfolders as shown in the Project Structure.

Navigate to the Project Directory:
Open your terminal or command prompt and change to your project's root directory:

cd path\to\rem_waste_accent_analyzer

(Replace path\to\rem_waste_accent_analyzer with your actual path)

Create and Activate a Python Virtual Environment (Highly Recommended):
A virtual environment isolates your project's dependencies, preventing conflicts with other Python projects.

python -m venv myenv

On Windows:

.\myenv\Scripts\activate

On macOS/Linux:

source myenv/bin/activate

You should see (myenv) at the beginning of your terminal prompt, indicating the virtual environment is active.

Install Python Dependencies:
With your virtual environment activated, install all required Python libraries. This step is crucial for resolving potential version compatibility issues.

# Uninstall existing versions for a clean slate (important!)
pip uninstall speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor yt-dlp -y

# Install the latest compatible versions
pip install --upgrade speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor yt-dlp

Note on UserWarning: You might see a UserWarning: Requested Pretrainer collection using symlinks on Windows... during model loading. This is an informational message from SpeechBrain/PyTorch/HuggingFace about internal file handling and can generally be ignored as it does not prevent the application from functioning.

Manual Hugging Face Cache Cleanup (Optional, if issues persist):
If you continue to face model loading errors after step 4, you might need to manually clear the Hugging Face cache.

Delete the entire folder at D:\Accent Detection\rem_waste\.hf_cache (or wherever your HF_HOME environment variable points to within your project).

Then, try running the application again. This will force a fresh download of the model files.

Usage
Run the Flask Application:
Ensure your virtual environment is active, then run the main application file:

python app.py

You will see output in your terminal indicating the Flask server is running, typically on http://127.0.0.1:5000/.

Access the Web Interface:
Open your web browser and navigate to the address provided by Flask (e.g., http://127.0.0.1:5000/).

Analyze an Accent:

Enter a public video URL (e.g., a YouTube video link, a Loom link, or a direct link to an MP4 file) into the "Video URL" input field.

Click the "Analyze Accent" button.

The application will display a status message ("Initiating analysis...", "Still processing...").

Once the analysis is complete, the detected English accent, a confidence score, and a brief summary will appear on the page.

Error Handling & Troubleshooting
"Video download failed: yt-dlp failed: ERROR: unable to open for writing: [Errno 2] No such file or directory...":

This usually indicates yt-dlp cannot write to the temporary directory.

Solution: Ensure the rem_waste_accent_analyzer folder and its temp_files subdirectory have full write permissions for your user account. The subprocess.run with cwd set in video_processing.py is designed to mitigate this, but underlying OS permissions can still interfere. Running your terminal/command prompt as Administrator might temporarily resolve this for testing.

"Error opening 'D:\...\audio_...wav': System error." (during accent detection):

This indicates SpeechBrain is having trouble accessing the audio file.

Solution: This was addressed by converting the path to a relative path (os.path.relpath) before passing it to detect_accent. Ensure your app.py and accent_analysis.py files are updated to the latest versions provided in the previous responses.

"Error loading SpeechBrain model: No huggingface_hub attribute cached_download" or "There is no such class as speechbrain.lobes.models.huggingface_wav2vec.HuggingFaceWav2Vec2":

These are version compatibility issues between SpeechBrain and its dependencies.

Solution: Follow the "Install Python Dependencies" step (Step 4) very carefully, including the pip uninstall command for a clean installation. If it persists, try the "Manual Hugging Face Cache Cleanup" (Step 5).

"Analysis completed successfully!" but no results on webpage:

This means the backend is working, but the frontend isn't displaying the data.

Solution: Ensure your templates/index.html file includes the latest showResults function as provided, which explicitly removes the hidden class and sets style.display = 'block' for the results container. Check your browser's developer console (F12) for any JavaScript errors or the console.log("Received data from backend:", data); output to see the exact data structure.

Technologies Used
Backend:

Flask: Python web framework.

Flask-Executor: For running background tasks.

yt-dlp: Video downloading.

FFmpeg: Audio extraction and conversion.

SpeechBrain: Open-source speech toolkit for accent classification.

PyTorch: Deep learning framework (underpins SpeechBrain).

Hugging Face Hub: For hosting and accessing pre-trained models.

Frontend:

HTML5

Tailwind CSS: Utility-first CSS framework for rapid UI development.

JavaScript (Fetch API for AJAX, DOM manipulation).

License
This project is open-source and available under the MIT License.