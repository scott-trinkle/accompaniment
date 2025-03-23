import os
import sys
from pathlib import Path

# Get the home directory
DOWNLOADS_DIR = str(Path.home() / "Downloads")

# Create a log file with timestamp
import datetime
log_file = os.path.join(DOWNLOADS_DIR, f"app_log_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.txt")

# Open the log file and redirect stdout and stderr
sys.stdout = open(log_file, "w", buffering=1)  # Line buffering
sys.stderr = sys.stdout

print('Setting up log')

import librosa
import tkinter as tk
import yt_dlp

import soundfile as sf
from tkinter import messagebox

# Get the path to FFmpeg inside the PyInstaller bundle
if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
    FFMPEG_PATH = os.path.join(sys._MEIPASS, "ffmpeg", "ffmpeg.exe" if os.name == "nt" else "ffmpeg")
else:  # Running as a normal script
    FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe" if os.name == "nt" else "ffmpeg")


def update_log(message):
    print(message)
    messagebox.showinfo('Status', message)


def process_audio(input_file, speed):
    y, sr = librosa.load(input_file)        

    # Slow down the audio (e.g., factor of 0.5 means slowing down by 50%)
    y_slow = librosa.effects.time_stretch(y, rate=speed)    

    return y_slow, sr


def download_best_audio(url):

    update_log('Downloading file...')

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{DOWNLOADS_DIR}/%(title)s.%(ext)s',
        'ffmpeg_location' : FFMPEG_PATH
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"        
    
    return filename


def slow_down_audio(input_file, speed):
    update_log('Loading file...')
    speed = speed / 100
    output_file = input_file.split('.mp3')[0] + f'_{speed:.2f}x' + '.mp3'
    
    y_slow, sr = process_audio(input_file, speed)

    update_log('Saving...')
    sf.write(output_file, y_slow, sr)

    update_log('Removing...')
    os.remove(input_file)    

    return output_file


def main():
    url = url_entry.get()
    speed = float(speed_entry.get())    

    filename = download_best_audio(url)
    if speed != 100.0:        
        slow_down_audio(filename, speed)

    update_log('Complete!')


# Create the main window
root = tk.Tk()
root.title("Youtube downloader")

window_width = 600
window_height = 600

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Default values
default_speed = 100.0
default_url = "https://youtu.be/fW86lcZJoUs?si=xp1MoI_A6IJdu6sM"

tk.Label(root, text="URL:").pack(padx=10, pady=5, anchor='w')
url_entry = tk.Entry(root, width=50)
url_entry.insert(0, default_url)  # Set default value
url_entry.pack(padx=10, pady=5, anchor='w')

tk.Label(root, text="Speed (%):").pack(padx=10, pady=5, anchor='w')
speed_entry = tk.Entry(root)
speed_entry.insert(0, str(default_speed))  # Set default value
speed_entry.pack(padx=10, pady=5, anchor='w')

# Create the save button
save_button = tk.Button(root, text="Save Data", command=main)
save_button.pack(pady=10)

# Start the main loop
root.mainloop()
