from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_format_18_url(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        format_18 = next((f for f in info.get("formats", []) if f.get("format_id") == "18"), None)
        return format_18.get("url") if format_18 else None

@app.route('/get-url', methods=['GET'])
def get_url():
    url = request.args.get("url")
    if not url:
        return "Missing 'url' query parameter", 400

    try:
        direct_url = get_format_18_url(url)
        if not direct_url:
            return "format_id 18 not available", 404
        return direct_url
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
