import librosa
import os
import sys
import tkinter as tk
import yt_dlp

import soundfile as sf

from tkinter import messagebox
from pathlib import Path

# Get the home directory
DOWNLOADS_DIR = str(Path.home() / "Downloads")

# Get the path to FFmpeg inside the PyInstaller bundle
if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
    FFMPEG_PATH = os.path.join(sys._MEIPASS, "ffmpeg", "ffmpeg.exe" if os.name == "nt" else "ffmpeg")
else:  # Running as a normal script
    FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe" if os.name == "nt" else "ffmpeg")


class RedirectText:
    """Redirects stdout (print statements) to a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)  # Append text to the end
        self.text_widget.see(tk.END)  # Auto-scroll to the bottom

    def flush(self):  
        pass  # Needed for compatibility with sys.stdout


def update_log(message):
    print(message)
    log_label.config(text=message)  # Update label text
    

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
    update_log('Adjusting speed...')
    speed = speed / 100
    output_file = input_file.split('.mp3')[0] + f'_{speed:.2f}x' + '.mp3'
    
    y, sr = librosa.load(input_file)    

    # Slow down the audio (e.g., factor of 0.5 means slowing down by 50%)
    y_slow = librosa.effects.time_stretch(y, rate=speed)    

    sf.write(output_file, y_slow, sr)
    os.remove(input_file)    

    return output_file


def main():
    url = url_entry.get()
    speed = float(speed_entry.get())    

    filename = download_best_audio(url)
    if speed != 100.0:
        update_log('passed if statement')
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

# Label for logs
tk.Label(root, text="Status:").pack(pady=5)
log_label = tk.Label(root, text="Waiting for action...", font=("Arial", 12))
log_label.pack()

# Text Widget for Logs
log_text = tk.Text(root, height=10, width=50, state=tk.NORMAL)
log_text.pack()

# Redirect stdout to log_text widget
sys.stdout = RedirectText(log_text)


# Start the main loop
root.mainloop()
