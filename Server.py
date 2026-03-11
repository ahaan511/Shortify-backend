from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import uuid

app = FastAPI()

class VideoRequest(BaseModel):
    youtube_url: str

@app.post("/generate-shorts")
def generate_shorts(req: VideoRequest):

    video_id = str(uuid.uuid4())
    video_file = f"{video_id}.mp4"

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
        ("00:00:10","00:00:30"),
        ("00:01:00","00:01:30"),
        ("00:02:00","00:02:30")
    ]

    for i,(start,end) in enumerate(timestamps):

        output = f"clip_{i}.mp4"

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
            output
        ])

        clips.append(output)

    return {"clips": clips}
