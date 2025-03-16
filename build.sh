#!/bin/sh

rm -r build
rm -r dist
rm YoutubeDownloder.spec

pyinstaller --onefile --windowed --clean --name YoutubeDownloader --add-data "ffmpeg/*:ffmpeg" app.py