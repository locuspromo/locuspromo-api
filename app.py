from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SOUNDCLOUD_CLIENT_ID = "w1OB6ERQK3sAH8CY"  # Public Client ID

@app.get("/recommend")
def recommend(mood: str = "lofi"):
    try:
        url = "https://api-v2.soundcloud.com/search/tracks"
        params = {
            "q": mood,
            "client_id": SOUNDCLOUD_CLIENT_ID,
            "limit": 10
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        tracks = res.json().get("collection", [])

        return [
            {
                "title": t.get("title"),
                "artist": t.get("user", {}).get("username"),
                "url": t.get("permalink_url"),
                "artwork": t.get("artwork_url")
            }
            for t in tracks
        ]
    except Exception as e:
        print("ERROR:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
