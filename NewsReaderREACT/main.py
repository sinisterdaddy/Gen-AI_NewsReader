from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from genvideo import genvideo
from downloadvideo import download_video
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Function to generate news and video based on the selected sport
def generate_news_and_video(sport):
    # Add your logic here to generate news based on the selected sport
    # For demonstration purposes, let's assume the news text is generated
    news_text = f"Latest news related to {sport}."

    # Generate video using genvideo
    id = genvideo("https://clips-presenters.d-id.com/amy/Aq6OmGZnMt/Vcq0R4a8F0/image.png", news_text, "en-US-SaraNeural")
    # Sleep for a while to allow the video to be processed
    time.sleep(100)
    # Download the video using download_video
    video_url = download_video(id)

    return video_url

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to generate news and video
@app.route('/generate_news_and_video', methods=['POST'])
def generate_news_video():
    # Get the selected sport from the request
    sport = request.json['sport']
    # Generate news and video based on the selected sport
    video_url = generate_news_and_video(sport)
    # Return the video URL in the response
    return jsonify(video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
