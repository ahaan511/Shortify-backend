from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Shortify backend running"}

@app.post("/generate-shorts")
def generate_shorts(data: dict):
    youtube_url = data.get("youtube_url")

    return {
        "clips": [
            {
                "title": "Clip 1",
                "start": "00:00:10",
                "end": "00:00:30",
                "download_url": "https://example.com/clip1.mp4"
            },
            {
                "title": "Clip 2",
                "start": "00:01:00",
                "end": "00:01:30",
                "download_url": "https://example.com/clip2.mp4"
            }
        ]
    }
