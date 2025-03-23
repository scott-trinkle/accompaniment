#!/bin/sh

rm -r build
rm -r dist
rm YoutubeDownloder.spec


export MACOSX_DEPLOYMENT_TARGET=11.7
echo $MACOSX_DEPLOYMENT_TARGET
pyinstaller --onefile --windowed --clean --name YoutubeDownloader --add-data "ffmpeg:ffmpeg" --hidden-import=numpy app.py