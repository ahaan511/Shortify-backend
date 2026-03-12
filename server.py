from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import os
import uuid

app = FastAPI()

# Allow requests from any frontend (Lovable, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where clips will be stored
CLIPS_DIR = "clips"
os.makedirs(CLIPS_DIR, exist_ok=True)

# Serve clips publicly
app.mount("/clips", StaticFiles(directory=CLIPS_DIR), name="clips")


@app.get("/")
def home():
    return {"message": "Shortify backend running"}


# Request model (accepts both url formats to avoid 422 errors)
class VideoRequest(BaseModel):
    url: str | None = None
    youtube_url: str | None = None


@app.post("/generate-clips")
def generate_clips(data: VideoRequest):

    # Accept either "url" or "youtube_url"
    video_url = data.url or data.youtube_url

    if not video_url:
        return {"error": "No video URL provided"}

    video_id = str(uuid.uuid4())
    video_file = f"{video_id}.mp4"

    # Download video
    subprocess.run([
        "yt-dlp",
        "-f",
        "mp4",
        "-o",
        video_file,
        video_url
    ])

    clips = []

    # Generate 3 clips (30s each)
    for i in range(3):
        start = i * 30
        clip_name = f"{CLIPS_DIR}/clip{i}_{video_id}.mp4"

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

        clips.append(f"/clips/clip{i}_{video_id}.mp4")

    return {"clips": clips}
