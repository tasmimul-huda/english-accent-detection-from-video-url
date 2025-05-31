
import math
import os
# SpeechBrain and its dependencies
from speechbrain.inference.classifiers import EncoderClassifier # Updated import as requested
import torch
import torchaudio
import numpy
import scipy
from tqdm import tqdm
from huggingface_hub import hf_hub_download
import torch.nn.functional as F

import warnings
warnings.filterwarnings("ignore")
# --- Global variable for the accent classification model ---
accent_classifier = None

# Define a temporary directory for Hugging Face cache within the current working directory
HF_CACHE_DIR = os.path.join(os.getcwd(), '.hf_cache')
os.makedirs(HF_CACHE_DIR, exist_ok=True) # Create the directory if it doesn't exist
print(f"Hugging Face cache directory created/ensured at: {HF_CACHE_DIR}")

# --- Function to load the SpeechBrain Accent Classification Model ---
def load_accent_model():
    """
    Loads the SpeechBrain accent classification model from Hugging Face.
    This function should be called once at application startup.
    """
    global accent_classifier
    if accent_classifier is None:
        try:
            print("Loading SpeechBrain accent classification model... This may take a moment.")

            # Set the HF_HOME environment variable to redirect Hugging Face's cache.
            # This is crucial for resolving WinError 1314 permission issues on Windows,
            # as it ensures model files are downloaded and cached in a user-writable location.
            os.environ['HF_HOME'] = HF_CACHE_DIR
            print(f"HF_HOME environment variable set to: {os.environ['HF_HOME']}")

            # Using the ECAPA-TDNN based model for English accent classification
            accent_classifier = EncoderClassifier.from_hparams(
                source="Jzuluaga/accent-id-commonaccent_ecapa",
                savedir="pretrained_models/accent-id-commonaccent_ecapa" # A distinct directory for this model
            )
            print("SpeechBrain model loaded successfully.")
        except Exception as e:
            print(f"Error loading SpeechBrain model: {e}")
            print("\n--------------------------------------------------------------")
            print("Troubleshooting Steps for Model Loading Errors:")
            print("1. **Ensure Python Environment is Clean:** If you haven't, create a NEW virtual environment and install dependencies there.")
            print("   Example (in your project directory):")
            # print("   `python -m venv new_accent_env`")
            # print("   `.\new_accent_env\Scripts\activate` (Windows) or `source new_accent_env/bin/activate` (macOS/Linux)")
            print("2. **Install/Upgrade ALL Dependencies:**")
            print("   `pip uninstall speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor yt-dlp -y`")
            print("   `pip install --upgrade speechbrain transformers torchaudio huggingface_hub numpy scipy tqdm Flask Flask-Executor`")
            # print("3. **Manually Clear Hugging Face Cache:** If issues persist, delete the folder: `D:\Accent Detection\rem_waste\.hf_cache`")
            print("   This forces a fresh download. Then try running your app again.")
            print("4. **Check FFmpeg Installation:** Ensure FFmpeg is installed on your system and its `bin` directory is added to your system's PATH.")
            print("--------------------------------------------------------------\n")
            accent_classifier = None # Set to None if loading fails

# --- Function to detect accent from an audio file ---
def detect_accent(audio_path, task_id):
    """
    Analyzes the speaker's accent from the given audio file using the pre-loaded SpeechBrain model.
    Returns the classified accent, a confidence score, and a summary.
    """
    if accent_classifier is None:
        return None, None, None, "Accent classification model not loaded. Please ensure the model loads correctly at startup."

    print(f"Task {task_id}: Analyzing accent from {audio_path}...")
    try:
        # The audio_path passed here from video_processing.py should already be an absolute path.
        # Removing os.path.abspath() to prevent potential double-concatenation issues
        # if SpeechBrain's internal file handling implicitly prepends CWD to an already absolute path.
        # processed_audio_path = os.path.abspath(audio_path) # Removed this line
        processed_audio_path = audio_path # Use the path directly as it should be absolute

        print(f"Task {task_id}: Final audio path for SpeechBrain: {processed_audio_path}")

        # Add checks for file existence and size
        if not os.path.exists(processed_audio_path):
            return None, None, None, f"Audio file not found at: {processed_audio_path}"
        if os.path.getsize(processed_audio_path) == 0:
            return None, None, None, f"Audio file is empty at: {processed_audio_path}"

        out_prob, score, index, text_lab = accent_classifier.classify_file(processed_audio_path)

        # Print raw outputs for debugging/understanding
        print(f"out_prob: {out_prob}, score: {score}, index: {index}, text_lab: {text_lab}")

        # Apply softmax to convert logits (out_prob) into probabilities.
        probabilities = F.softmax(out_prob, dim=-1)

        # Get the confidence for the predicted accent
        confidence = probabilities[0, index.item()] * 100

        accent = text_lab[0]
        summary = "Analysis complete. The detected accent is based on the dominant English accent identified in the audio segment provided."

        print(f"Task {task_id}: Accent: {accent}, Confidence: {confidence:.2f}%")
        return accent, confidence, summary, None

    except Exception as e:
        error_message = f"An error occurred during accent detection: {e}"
        print(f"Task {task_id}: {error_message}")
        return None, None, None, error_message



# Example of how you would integrate this (not runnable on its own, requires an audio file)
if __name__ == '__main__':
    # This part is for demonstration and would be integrated into your Flask app.
    # You would need an actual audio file (e.g., a .wav file) to test this.
    # For example:
    HF_CACHE_DIR = os.path.join(os.getcwd(), '.hf_cache')
    os.makedirs(HF_CACHE_DIR, exist_ok=True) # Create the directory if it doesn't exist
    print(f"Hugging Face cache directory created/ensured at: {HF_CACHE_DIR}")
    input_file = input("Enter audio: ")
    dummy_audio_path = f"temp_files/{input_file}"
    test_task_id = "test_accent_detection_123"

    # 1. Load the model first (typically done once at app startup)
    load_accent_model()

    # 2. Then call detect_accent with a valid audio path
    if accent_classifier:
        accent, confidence, summary, error = detect_accent(dummy_audio_path, test_task_id)
        if accent:
            print(f"\n--- Detection Result ---")
            print(f"Detected Accent: {accent}")
            print(f"Confidence: {confidence:.2f}%")
            print(f"Summary: {summary}")
        else:
            print(f"\n--- Detection Error ---")
            print(f"Error: {error}")
    else:
        print("Model could not be loaded, skipping accent detection example.")
