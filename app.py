import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

# Create a folder to store downloads
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Options for yt-dlp
def get_ydl_opts(format_choice):
    opts = {
        "format": "bestaudio/best" if format_choice == "mp3" else "best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    }
    if format_choice == "mp3":
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
        opts["ffmpeg_location"] = "/usr/bin/ffmpeg"  # Set FFmpeg path
    return opts

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        format_choice = request.form["format"]

        try:
            with yt_dlp.YoutubeDL(get_ydl_opts(format_choice)) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).replace(".webm", f".{format_choice}")

            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
