import os
import subprocess
import uuid

def download_video(video_url, task_id, temp_dir):
    """
    Downloads a video from the given URL to a temporary file.
    Uses yt-dlp for robust video downloading.
    Returns the path to the downloaded video or None if an error occurs.
    """
    video_path = None
    try:
        print(f"Task {task_id}: Starting video download for {video_url}")

        # Ensure temp_dir is an absolute and normalized path
        # This is a defensive step, as it should already be absolute from app.py
        normalized_temp_dir = os.path.abspath(temp_dir)
        os.makedirs(normalized_temp_dir, exist_ok=True) # Ensure the base temp directory exists

        # Generate a unique filename for the video
        video_filename = f"video_{uuid.uuid4()}.mp4"
        video_path = os.path.join(normalized_temp_dir, video_filename)

        # Ensure the target directory for the video file exists right before attempting to write
        # This is redundant if normalized_temp_dir is already created, but harmless.
        # os.makedirs(os.path.dirname(video_path), exist_ok=True) # This line is now less critical
        print(f"Task {task_id}: Ensuring directory exists for video: {os.path.dirname(video_path)}")
        print(f"Task {task_id}: Attempting to write video to: {video_path}")


        # yt-dlp options: download best audio/video format, output to specified path
        yt_dlp_options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': video_path, # Use the absolute video_path here
            'noplaylist': True, # Only download single video, not playlists
            'quiet': True, # Suppress console output from yt-dlp
            'no_warnings': True, # Suppress warnings from yt-dlp
        }

        # Use subprocess to run yt-dlp command.
        command = ['yt-dlp', '-f', yt_dlp_options['format'], '-o', yt_dlp_options['outtmpl'], video_url]
        if yt_dlp_options['noplaylist']:
            command.append('--no-playlist')
        if yt_dlp_options['quiet']:
            command.append('--quiet')
        if yt_dlp_options['no_warnings']:
            command.append('--no-warnings')

        print(f"Task {task_id}: yt-dlp command: {' '.join(command)}") # <-- NEW: Print the command

        process = subprocess.run(command, capture_output=True, text=True, check=False)

        if process.returncode != 0:
            error_message = f"yt-dlp failed: {process.stderr.strip()}"
            print(f"Task {task_id}: {error_message}")
            return None, error_message

        if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
            error_message = "Video download failed or resulted in an empty file."
            print(f"Task {task_id}: {error_message}")
            return None, error_message

        print(f"Task {task_id}: Video downloaded to {video_path}")
        return video_path, None

    except Exception as e:
        error_message = f"An error occurred during video download: {e}"
        print(f"Task {task_id}: {error_message}")
        return None, error_message


def extract_audio(video_path, task_id, temp_dir):
    """
    Extracts audio from the given video file to a temporary WAV file.
    Uses FFmpeg for robust audio extraction and conversion.
    Returns the path to the extracted audio or None if an error occurs.
    """
    audio_path = None
    try:
        print(f"Task {task_id}: Extracting audio from video...")
        # Generate a unique filename for the audio
        audio_filename = f"audio_{uuid.uuid4()}.wav"
        audio_path = os.path.join(temp_dir, audio_filename)

        # FFmpeg command to extract audio as 16kHz mono WAV
        ffmpeg_command = [
            'ffmpeg', '-i', video_path, '-ar', '16000', '-ac', '1', '-vn', '-y', audio_path
        ]
        print(f"Task {task_id}: FFmpeg command: {' '.join(ffmpeg_command)}") # <-- NEW: Print the command
        process = subprocess.run(ffmpeg_command, capture_output=True, text=True, check=False)

        if process.returncode != 0:
            error_message = f"FFmpeg audio extraction failed: {process.stderr.strip()}"
            print(f"Task {task_id}: {error_message}")
            return None, error_message

        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            error_message = "Audio extraction failed or resulted in an empty file."
            print(f"Task {task_id}: {error_message}")
            return None, error_message

        print(f"Task {task_id}: Audio extracted to {audio_path}")
        return audio_path, None

    except Exception as e:
        error_message = f"An error occurred during audio extraction: {e}"
        print(f"Task {task_id}: {error_message}")
        return None, error_message



# # Example Usage (for demonstration, not part of the Flask app flow directly)
# if __name__ == '__main__':
#     TEMP_DIR = os.path.join(os.getcwd(), 'temp_folder')
#     os.makedirs(TEMP_DIR, exist_ok=True) # Create the directory if it doesn't exist
#     print(f"Temporary directory created/ensured at: {TEMP_DIR}")

#     # You would replace this with an actual video URL for testing
#     # test_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Example YouTube URL
#     test_video_url = input("ENter video link: ")
#     test_task_id = "test_task_123"

#     downloaded_video_path, download_error = download_video(test_video_url, test_task_id, TEMP_DIR)

#     if downloaded_video_path:
#         extracted_audio_path, extract_error = extract_audio(downloaded_video_path, test_task_id, TEMP_DIR)

#         if extracted_audio_path:
#             print(f"Successfully downloaded video to: {downloaded_video_path}")
#             print(f"Successfully extracted audio to: {extracted_audio_path}")
#         else:
#             print(f"Audio extraction failed: {extract_error}")

#         # Clean up after testing
#         # cleanup_temp_files(downloaded_video_path) # This would be handled by the main app's finally block
#         # cleanup_temp_files(extracted_audio_path) # This would be handled by the main app's finally block
#     else:
#         print(f"Video download failed: {download_error}")

#     # Clean up the entire temp_files directory if it's the end of the application lifecycle
#     # shutil.rmtree(TEMP_DIR)
#     # print(f"Temporary direc