from flask import Flask, request, render_template, send_file
import yt_dlp
import ffmpeg
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['url']
        temp_id = str(uuid.uuid4())
        video_file = f"{temp_id}.mp4"
        output_file = f"{temp_id}.3gp"

        try:
            ydl_opts = {
                'format': 'worst',
                'outtmpl': video_file,
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            ffmpeg.input(video_file).output(
                output_file,
                format='3gp',
                vf='scale=176:144',
                acodec='aac',
                vcodec='mpeg4',
                video_bitrate='100k',
                audio_bitrate='32k'
            ).overwrite_output().run()

            os.remove(video_file)
            return send_file(output_file, as_attachment=True)

        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
