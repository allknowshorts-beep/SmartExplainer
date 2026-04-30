from flask import Flask, request, jsonify
from gtts import gTTS
from moviepy.editor import *
import requests
import os

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic", "science")

    # simple script
    text = f"This is a short explanation about {topic}"

    # voice
    tts = gTTS(text)
    tts.save("voice.mp3")

    # image
    img_url = f"https://source.unsplash.com/800x600/?{topic}"
    img_data = requests.get(img_url).content
    with open("image.jpg", "wb") as f:
        f.write(img_data)

    # video
    clip = ImageClip("image.jpg").set_duration(5)
    audio = AudioFileClip("voice.mp3")
    video = clip.set_audio(audio)

    video.write_videofile("output.mp4", fps=24)

    return jsonify({"status": "done"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)