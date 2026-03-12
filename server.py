from pydantic import BaseModel

class VideoRequest(BaseModel):
    url: str | None = None
    youtube_url: str | None = None


@app.post("/generate-clips")
def generate_clips(data: VideoRequest):

    url = data.url or data.youtube_url

    if not url:
        return {"error": "No video URL provided"}

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
