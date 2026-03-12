from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import os
import uuid

app = FastAPI()

# CORS for Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# clips folder
CLIPS_DIR = "clips"
os.makedirs(CLIPS_DIR, exist_ok=True)

app.mount("/clips", StaticFiles(directory=CLIPS_DIR), name="clips")


@app.get("/")
def home():
    return {"message": "Shortify backend running"}


class VideoRequest(BaseModel):
    url: str | None = None
    youtube_url: str | None = None


@app.post("/generate-clips")
def generate_clips(data: VideoRequest):

    try:
        video_url = data.url or data.youtube_url

        if not video_url:
            return {"error": "No URL provided"}

        video_id = str(uuid.uuid4())
        video_file = f"{video_id}.mp4"

        # download youtube video
        download = subprocess.run(
            ["python", "-m", "yt_dlp", "-f", "mp4", "-o", video_file, video_url],
            capture_output=True,
            text=True
        )

        if download.returncode != 0:
            return {"error": "yt-dlp failed", "details": download.stderr}

        clips = []

        # create 3 clips
        for i in range(3):
            start = i * 30
            clip_name = f"{CLIPS_DIR}/clip{i}_{video_id}.mp4"

            cut = subprocess.run(
                [
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
                ],
                capture_output=True,
                text=True
            )

            if cut.returncode != 0:
                return {"error": "ffmpeg failed", "details": cut.stderr}

            clips.append(f"/clips/clip{i}_{video_id}.mp4")

        return {"clips": clips}

    except Exception as e:
        return {"error": str(e)}
