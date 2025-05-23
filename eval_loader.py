import os
import csv
import subprocess
from pathlib import Path
from yt_dlp import YoutubeDL
from pydub.utils import mediainfo

# Set paths
CSV_FILE = 'eval_segments.csv'
OUTPUT_DIR = Path('audioset/eval')
LOG_FILE = OUTPUT_DIR / 'downloaded.log'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load already downloaded IDs
if LOG_FILE.exists():
    with open(LOG_FILE, 'r') as logf:
        downloaded = set(line.strip() for line in logf)
else:
    downloaded = set()

def mark_downloaded(entry):
    with open(LOG_FILE, 'a') as logf:
        logf.write(entry + '\n')

# Function to download and trim audio
def download_and_trim_audio(youtube_id, start_seconds, end_seconds, output_path):
    temp_file = OUTPUT_DIR / f"{youtube_id}.temp.m4a"
    try:
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

        cmd = [
            'ffmpeg', '-y',
            '-i', str(temp_file),
            '-ss', str(start_seconds),
            '-to', str(end_seconds),
            '-ar', '16000',
            '-ac', '1',
            str(output_path)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        info = mediainfo(output_path)
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
            continue
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 3:
            continue

        try:
            youtube_id = parts[0]
            start_time = float(parts[1])
            end_time = float(parts[2])
            output_name = f"{youtube_id}_{int(start_time)}.wav"
            output_path = OUTPUT_DIR / output_name

            if output_name in downloaded:
                continue

            sr = download_and_trim_audio(youtube_id, start_time, end_time, output_path)
            if sr:
                print(f"Saved: {output_path.name}, Sample Rate: {sr}")
                mark_downloaded(output_name)

        except ValueError as ve:
            print(f"Skipping malformed row: {parts} - {ve}")
