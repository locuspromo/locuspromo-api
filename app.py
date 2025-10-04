from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jamendo API key (replace with your own)
JAMENDO_CLIENT_ID = "YOUR_JAMENDO_CLIENT_ID"

@app.get("/recommend")
def recommend(mood: str = "chill"):
    try:
        url = "https://api.jamendo.com/v3.0/tracks"
        params = {
            "client_id": JAMENDO_CLIENT_ID,
            "format": "json",
            "limit": 10,
            "tags": mood,
            "fuzzytags": "1",
            "audioformat": "mp31",
            "include": "musicinfo",
            "groupby": "artist_id",
            "order": "popularity_total"
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        tracks = res.json().get("results", [])

        return [
            {
                "title": t.get("name"),
                "artist": t.get("artist_name"),
                "url": t.get("audio"),
                "album": t.get("album_name"),
                "image": t.get("album_image")
            }
            for t in tracks
        ]

    except Exception as e:
        print("ERROR:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
