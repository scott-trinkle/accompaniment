# YouTube Downloader

- Downloaded ffmpeg [here](https://evermeet.cx/ffmpeg/)
- Removed quarantine: `xattr -d com.apple.quarantine /path/to/ffmpeg`
- Signed the executable: `codesign --force --deep --sign - /path/to/ffmpeg`