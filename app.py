from flask import Flask, request
import yt_dlp
import os

app = Flask(__name__)

COOKIE_PATH = os.path.join(os.getcwd(), "cookies.txt")  # ./cookies.txt in project root

def get_format_18_url(url):
    # Ensure cookie file exists
    if not os.path.exists(COOKIE_PATH):
        raise FileNotFoundError(f"cookies.txt not found at: {COOKIE_PATH}")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "cookiefile": COOKIE_PATH,  # pass cookies to yt-dlp
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
        # Return only the URL (plain text)
        return direct_url, 200, {"Content-Type": "text/plain; charset=utf-8"}
    except FileNotFoundError as e:
        return str(e), 500
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
