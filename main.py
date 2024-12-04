from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    quality = request.form['quality']  # Pilihan kualitas video

    try:
        # Konfigurasi yt-dlp
        ydl_opts = {
            'format': 'best' if quality == 'high' else 'worst',  # Pilih format video
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Lokasi unduhan
        }

        # Proses unduhan dengan yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)  # Path file video

        # Kirim file ke user
        return send_file(
            file_path,
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )

    except Exception as e:
        return f"Terjadi kesalahan: {e}"

if __name__ == "__main__":
    # Buat folder downloads jika belum ada
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)