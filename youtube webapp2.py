from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Directory to save downloaded videos
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# HTML template with dark theme
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            text-align: center;
            background-color: #1e1e1e;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.7);
        }

        h1 {
            color: #f1c40f;
        }

        input[type="text"] {
            width: 80%;
            padding: 10px;
            border-radius: 5px;
            border: none;
            margin-bottom: 20px;
            background-color: #333;
            color: #ffffff;
        }

        select {
            width: 80%;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            background-color: #333;
            color: #ffffff;
        }

        button {
            padding: 12px 24px;
            border-radius: 5px;
            background-color: #f1c40f;
            border: none;
            color: #1e1e1e;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background-color: #f39c12;
        }

        .footer {
            margin-top: 20px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Downloader</h1>
        <form action="/download" method="POST">
            <input type="text" name="url" placeholder="Enter YouTube URL" required><br>
            <select name="quality" required>
                <option value="" disabled selected>Select Quality</option>
                <option value="137">1080p</option>
                <option value="136">720p</option>
                <option value="135">480p</option>
                <option value="134">360p</option>
                <option value="140">Audio (Medium Quality)</option>
                <option value="139">Audio (Low Quality)</option>
            </select><br>
            <button type="submit">Download</button>
        </form>
        <div class="footer">
            <p>Made footage fusion ❤️</p>
        </div>
    </div>
</body>
</html>
"""

# Home route that renders the HTML form
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route to handle video download
@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    quality = request.form['quality']

    ydl_opts = {
        'format': quality,  # User-selected format
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, 'downloaded_video.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Find the downloaded video in the folder
    for file_name in os.listdir(DOWNLOAD_FOLDER):
        if file_name.startswith('downloaded_video'):
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
            return send_file(file_path, as_attachment=True)

    return "Error: Video not downloaded!"

if __name__ == '__main__':
    app.run(debug=True)
