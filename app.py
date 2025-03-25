import os
from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL

app = Flask(__name__)

# FFmpeg Path (Downloaded in render-build.sh)
FFMPEG_PATH = os.path.abspath("ffmpeg/ffmpeg")


def download_video(url, format_type):
    """Downloads YouTube video in the specified format."""
    ydl_opts = {
        "format": "bestvideo+bestaudio/best" if format_type == "mp4" else "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "ffmpeg_location": FFMPEG_PATH,  # Use custom FFmpeg path
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}] if format_type == "mp3" else [],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        if format_type == "mp3":
            filename = filename.rsplit(".", 1)[0] + ".mp3"
    
    return filename


@app.route("/", methods=["GET", "POST"])
def index():
    """Handles form submission and downloads video."""
    if request.method == "POST":
        url = request.form.get("url")
        format_type = request.form.get("format", "mp4")

        if not url:
            return render_template("index.html", error="Please enter a valid YouTube URL.")

        try:
            filepath = download_video(url, format_type)
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return render_template("index.html", error=f"Error: {e}")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
