import io
import os
import yt_dlp
import numpy as np
import streamlit as st
import librosa
from pydub import AudioSegment


# FFMPEG_PATH = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg")

# # Set the path to ffmpeg (if it's not in your PATH)
# os.environ["FFMPEG_BINARY"] = FFMPEG_PATH


def download_best_audio(url, output_dir="."): 
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        # 'ffmpeg_location' : FFMPEG_PATH,
        # 'ffprobe_location': FFMPEG_PATH
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"

    thumbnail_url = info.get("thumbnail", "")

    y, sr = librosa.load(filename)
    output_file = filename.split('.mp3')[0] + f'_{speed}' + '.mp3'

    os.remove(filename)
    
    return y, sr, output_file


def audio_arr_to_bin(arr, sr):
    arr = np.int16(arr / np.max(np.abs(arr)) * 32767)

    # Convert processed audio (NumPy array) to WAV using pydub
    audio_segment = AudioSegment(
        arr.tobytes(),
        frame_rate=sr,
        sample_width=2,  # 16-bit audio
        channels=1       # Mono audio
    )

    # Save the processed audio to a BytesIO buffer as MP3
    mp3_buffer = io.BytesIO()
    audio_segment.export(mp3_buffer, format="mp3")
    mp3_buffer.seek(0)  # Reset the buffer position to the beginning
    return mp3_buffer


def slow_down_audio(y, speed):
    speed = speed / 100        

    # Slow down the audio (e.g., factor of 0.5 means slowing down by 50%)
    y_slow = librosa.effects.time_stretch(y, rate=speed)

    return y_slow


st.title('Download accompaniment tracks')


with st.form('input form'):
    url = st.text_input('URL', value='')
    speed = st.number_input('% Speed', min_value=1, max_value=500, value=100)
    st.form_submit_button('Update')

if url != '':
    run_yt = st.button(f'Click to load file and change to {speed/100:.2f}x speed')
    status = st.empty()
    if run_yt:
        status.warning('Loading audio...')    
        y, sr, out_fn = download_best_audio(url)
    
        if speed != 100:
            status.warning('Adjusting speed...')
            y = slow_down_audio(y, speed=speed)

        status.success('Your file is ready to download')

        mp3_buffer = audio_arr_to_bin(y, sr)
        
        st.download_button(
            label="Download file",
            data=mp3_buffer,
            file_name=out_fn,
            mime="audio/mp3"
        )