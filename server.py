from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIPS_DIR = "clips"
os.makedirs(CLIPS_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Shortify backend running"}


@app.post("/generate-clips")
def generate_clips(url: str):

    video_id = str(uuid.uuid4())
    video_file = f"{video_id}.mp4"

    subprocess.run([
        "yt-dlp",
        "-f",
        "mp4",
        "-o",
        video_file,
        url
    ])

    clips = []

    for i in range(3):
        start = i * 30
        clip_name = f"{CLIPS_DIR}/clip{i}.mp4"

        subprocess.run([
            "ffmpeg",
            "-i",
            video_file,
            "-ss",
            str(start),
            "-t",
            "30",
            "-c",
            "copy",
            clip_name
        ])

        clips.append(f"/clips/clip{i}.mp4")

    return {"clips": clips}
