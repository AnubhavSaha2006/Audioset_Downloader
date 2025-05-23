import os
import csv
import subprocess
from pathlib import Path
from yt_dlp import YoutubeDL
from pydub.utils import mediainfo

# Set paths
CSV_FILE = 'eval_segments.csv'
OUTPUT_DIR = Path('audioset/eval')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
COMPLETED_FILE = OUTPUT_DIR / 'completed.txt'

# Load completed IDs
completed = set()
if COMPLETED_FILE.exists():
    with open(COMPLETED_FILE, 'r') as f:
        completed = set(line.strip() for line in f)

# Function to download and trim audio
def download_and_trim_audio(youtube_id, start_seconds, end_seconds, output_path):
    temp_file = OUTPUT_DIR / f"{youtube_id}.temp.m4a"
    output_file = output_path

    try:
        # Download audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': str(temp_file),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={youtube_id}"])

        # Trim audio with ffmpeg
        cmd = [
            'ffmpeg', '-y',
            '-i', str(temp_file),
            '-ss', str(start_seconds),
            '-to', str(end_seconds),
            '-ar', '16000',  # Resample to 16kHz
            '-ac', '1',      # Mono
            str(output_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        info = mediainfo(output_file)
        return info.get('sample_rate', 'unknown')

    except Exception as e:
        print(f"Error processing {youtube_id}: {e}")
        return None
    finally:
        if temp_file.exists():
            temp_file.unlink()

# Process CSV
with open(CSV_FILE, 'r') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue  # Skip comments and empty lines
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 3:
            continue  # Skip malformed lines

        try:
            youtube_id = parts[0]
            if youtube_id in completed:
                continue

            start_time = float(parts[1])
            end_time = float(parts[2])
            output_path = OUTPUT_DIR / f"{youtube_id}_{int(start_time)}.wav"

            if output_path.exists():
                completed.add(youtube_id)
                continue

            sr = download_and_trim_audio(youtube_id, start_time, end_time, output_path)
            if sr:
                print(f"Saved: {output_path.name}, Sample Rate: {sr}")
                with open(COMPLETED_FILE, 'a') as cf:
                    cf.write(youtube_id + '\n')
                completed.add(youtube_id)
        except ValueError as ve:
            print(f"Skipping malformed row: {parts} - {ve}")
