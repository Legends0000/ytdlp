import os
from flask import Flask, request, send_file
import yt_dlp
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return '''
        <h2>YouTube to 3GP (176x144) Downloader</h2>
        <form method="POST" action="/download">
            YouTube URL: <input name="url" required><br><br>
            <button type="submit">Download 3GP</button>
        </form>
    '''

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    file_name = f"{uuid.uuid4()}.3gp"

    ydl_opts = {
        'format': '160',  # 3gp 176x144 (itag 160)
        'outtmpl': file_name,
        'quiet': True,
        'proxy': 'http://103.231.80.146:55443',  # ✅ Free working HTTP proxy
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"<b>Error:</b> {str(e)}"

    return send_file(file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
