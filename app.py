from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    download_type = request.form.get('type')

    if not url or not download_type:
        return "Missing data"

    temp_filename = str(uuid.uuid4())

    ydl_opts = {}

    if download_type == "video":
        ydl_opts = {
            'outtmpl': f'{temp_filename}.mp4',
            'format': 'bestvideo+bestaudio/best'
        }
    elif download_type == "audio":
        ydl_opts = {
            'outtmpl': f'{temp_filename}.mp3',
            'format': 'bestaudio[ext=mp3]/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        return "Invalid type"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file_path = f"{temp_filename}.{'mp3' if download_type == 'audio' else 'mp4'}"
        return send_file(file_path, as_attachment=True)
    finally:
        if os.path.exists(f"{temp_filename}.mp4"):
            os.remove(f"{temp_filename}.mp4")
        if os.path.exists(f"{temp_filename}.mp3"):
            os.remove(f"{temp_filename}.mp3")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
