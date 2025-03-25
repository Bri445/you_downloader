#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Download and extract FFmpeg (no need for apt-get)
mkdir -p ffmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ --strip-components=1 -C ffmpeg

# Make FFmpeg executable
chmod +x ffmpeg/ffmpeg ffmpeg/ffprobe
