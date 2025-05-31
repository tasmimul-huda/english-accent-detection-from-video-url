import os
import subprocess
import uuid
import shutil
from flask import Flask, request, jsonify, render_template
from flask_executor import Executor

# Import modular functions
from video_processing import download_video, extract_audio
from accent_analysis import load_accent_model, detect_accent, HF_CACHE_DIR

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
# --- Flask Application Setup ---
app = Flask(__name__)
app.config['EXECUTOR_TYPE'] = 'thread' # Use threads for background tasks
app.config['EXECUTOR_MAX_WORKERS'] = 5 # Limit concurrent tasks
executor = Executor(app)

# --- Global Variables for Temporary Files ---
# Define a temporary directory within the current working directory
TEMP_DIR = os.path.join(os.getcwd(), 'temp_files')
os.makedirs(TEMP_DIR, exist_ok=True) # Create the directory if it doesn't exist
print(f"Temporary directory for media created/ensured at: {TEMP_DIR}")

# Ensure Hugging Face cache directory is created (this is handled by accent_analysis.py too, but good to ensure)
os.makedirs(HF_CACHE_DIR, exist_ok=True)
print(f"Hugging Face cache directory created/ensured at: {HF_CACHE_DIR}")

# --- Load the Accent Classification Model on App Startup ---
# This is crucial to load the model once and avoid repeated loading for each request.
with app.app_context():
    load_accent_model()


ACCENT_MAP = {
    "australia": "Australian",
    "canada": "Canadian",
    "england": "British",
    "us": "American",
    "philippines": "Filipino",
    "africa": "South African",
    "newzealand": "New Zealand",
    "ireland": "Irish",
    "scotland": "Scottish",
    "wales": "Welsh",
    "malaysia": "Malaysian",
    "singapore": "Singaporean",
    "bermuda": "Bermudian",
    "hongkong": "Hong Kong",
    "india": "Indian",
    "southatlandtic": "South Atlantic"
}

# --- Helper Function to Clean Up Temporary Files ---
def cleanup_temp_files(file_path):
    """
    Removes a file from the temporary directory.
    Ensures that only files within TEMP_DIR are removed.
    Does NOT remove entire directories.
    """
    if file_path and os.path.exists(file_path):
        try:
            abs_temp_dir = os.path.abspath(TEMP_DIR)
            abs_file_path = os.path.abspath(file_path)

            if abs_file_path.startswith(abs_temp_dir):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    app.logger.info(f"Cleaned up file: {file_path}")
                else:
                    app.logger.warning(f"Skipping cleanup of non-file: {file_path}")
            else:
                app.logger.warning(f"Attempted to clean up file outside designated temp directory: {file_path}")
        except Exception as e:
            app.logger.error(f"Error cleaning up {file_path}: {e}")

# --- Core Logic for Video Processing and Accent Analysis (Background Task) ---
def process_video_and_analyze_accent(video_url, task_id):
    """
    Downloads a video, extracts its audio, and classifies the English accent.
    This function runs in a background thread managed by Flask-Executor.
    """
    video_path = None
    audio_path = None
    try:
        # 1. Download Video
        app.logger.info(f"Task {task_id}: Starting video download for {video_url}")
        video_path, download_error = download_video(video_url, task_id, TEMP_DIR)
        if download_error:
            return {"status": "error", "message": f"Video download failed: {download_error}"}
        app.logger.info(f"Task {task_id}: Video downloaded to {video_path}")

        # 2. Extract Audio
        app.logger.info(f"Task {task_id}: Extracting audio from video...")
        audio_path, extract_error = extract_audio(video_path, task_id, TEMP_DIR)
        if extract_error:
            return {"status": "error", "message": f"Audio extraction failed: {extract_error}"}
        app.logger.info(f"Task {task_id}: Audio extracted to {audio_path}")

        # --- IMPORTANT CHANGE: Convert absolute audio_path to relative path ---
        # This is to work around potential issues where SpeechBrain might
        # implicitly prepend the current working directory to the path.
        relative_audio_path = os.path.relpath(audio_path, os.getcwd())
        app.logger.info(f"Task {task_id}: Relative audio path for SpeechBrain: {relative_audio_path}")


        # 3. Classify Accent
        app.logger.info(f"Task {task_id}: Analyzing accent...")
        # Pass the relative_audio_path to the detect_accent function
        accent, confidence, summary, accent_error = detect_accent(relative_audio_path, task_id)
        if accent_error:
            return {"status": "error", "message": f"Accent analysis failed: {accent_error}"}

        app.logger.info(f"Task {task_id}: Accent: {accent}, Confidence: {confidence:.2f}%")

        predicted_accent = ACCENT_MAP.get(accent)

        return {
            "status": "completed",
            "accent": predicted_accent,
            "confidence": f"{confidence:.2f}%",
            "summary": summary
        }

    except Exception as e:
        error_message = f"An unexpected error occurred during processing: {e}"
        app.logger.error(f"Task {task_id}: {error_message}", exc_info=True)
        return {"status": "error", "message": error_message}
    finally:
        # Clean up temporary files regardless of success or failure
        cleanup_temp_files(video_path)
        cleanup_temp_files(audio_path)

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    """
    Endpoint to receive video URL and initiate background accent analysis.
    Returns a task ID to the client.
    """
    data = request.get_json()
    video_url = data.get('video_url')
    app.logger.info(f"video url received: {video_url}")


    if not video_url:
        return jsonify({"status": "error", "message": "No video URL provided."}), 400

    # Generate a unique task ID
    task_id = str(uuid.uuid4())

    # Submit the long-running task to the executor
    executor.submit_stored(task_id, process_video_and_analyze_accent, video_url, task_id)

    return jsonify({"status": "processing", "task_id": task_id, "message": "Analysis started."}), 202

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    """
    Endpoint to check the status of a submitted task.
    Returns progress or final results.
    """
    if not executor.futures.done(task_id):
        # Task is still running or pending
        return jsonify({"status": "processing", "message": "Still processing..."}), 200
    else:
        # Task is completed (successfully or with error)
        future = executor.futures.pop(task_id) # Get and remove the future from storage
        try:
            result = future.result() # Get the result of the task
            return jsonify(result), 200
        except Exception as e:
            app.logger.error(f"Error retrieving result for task {task_id}: {e}", exc_info=True)
            return jsonify({"status": "error", "message": f"Failed to retrieve task result: {e}"}), 500

# --- Application Shutdown Hook (Optional but Recommended for Cleanup) ---
# @app.teardown_appcontext
# def teardown(exception=None):
#     """
#     Application shutdown hook — does NOT delete the temp directories.
#     Let background tasks finish safely without losing working directories.
#     """
#     print("App context is shutting down. Skipping deletion of TEMP_DIR and HF_CACHE_DIR to allow pending tasks to complete.")


# --- Main entry point for running the Flask app ---
if __name__ == '__main__':
    # When running locally, use debug=True for development.
    print(f"Starting Flask app from current working directory: {os.getcwd()}") # Added for debugging
    app.run(debug=True, host='0.0.0.0', port=5000)