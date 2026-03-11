from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    youtube_url: str


@app.get("/")
def home():
    return {"message": "Shortify backend running"}


@app.post("/generate-shorts")
def generate_shorts(req: VideoRequest):

    video_id = str(uuid.uuid4())
    video_file = f"{video_id}.mp4"

    # Download YouTube video
    subprocess.run([
        "yt-dlp",
        "-f",
        "mp4",
        "-o",
        video_file,
        req.youtube_url
    ])

    clips = []

    timestamps = [
        ("00:00:10", "00:00:30"),
        ("00:01:00", "00:01:30")
    ]

    for i, (start, end) in enumerate(timestamps):

        clip_file = f"clip_{i}_{video_id}.mp4"

        subprocess.run([
            "ffmpeg",
            "-ss",
            start,
            "-to",
            end,
            "-i",
            video_file,
            "-vf",
            "scale=1080:1920",
            clip_file
        ])

        clips.append({
            "title": f"Clip {i+1}",
            "start": start,
            "end": end,
            "download_url": clip_file
        })

    return {"clips": clips}
