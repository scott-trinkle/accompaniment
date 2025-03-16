import os
import sys
import tkinter as tk
import yt_dlp

from tkinter import messagebox
from pathlib import Path

# https://youtu.be/fW86lcZJoUs?si=xp1MoI_A6IJdu6sM

# Get the home directory
DOWNLOADS_DIR = str(Path.home() / "Downloads")

# Get the path to FFmpeg inside the PyInstaller bundle
if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
    FFMPEG_PATH = os.path.join(sys._MEIPASS, "ffmpeg", "ffmpeg.exe" if os.name == "nt" else "ffmpeg")
else:  # Running as a normal script
    FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe" if os.name == "nt" else "ffmpeg")


def download_best_audio():
    url = url_entry.get()

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

        messagebox.showinfo("Success", "Data saved successfully!")    
    
    return filename

# Create the main window
root = tk.Tk()
root.title("Youtube downloader")

# Default values
default_speed = 100.0
default_url = ""

tk.Label(root, text="URL:").pack(pady=5)
url_entry = tk.Entry(root)
url_entry.insert(0, default_url)  # Set default value
url_entry.pack(pady=5)

# # Create labels and entry fields
# tk.Label(root, text="Speed (%):").pack(pady=5)
# float_entry = tk.Entry(root)
# float_entry.insert(0, str(default_float))  # Set default value
# float_entry.pack(pady=5)

# Create the save button
save_button = tk.Button(root, text="Save Data", command=download_best_audio)
save_button.pack(pady=10)

# Start the main loop
root.mainloop()
