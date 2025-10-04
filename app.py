from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # ✅ MOVE THIS UP HERE
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIUS_API = "https://discoveryprovider.audius.io/v1"

@app.get("/recommend")
def recommend(mood: str = "lofi"):
    try:
        res = requests.get(f"{AUDIUS_API}/tracks/trending", params={"app_name": "locuspromo"})
        res.raise_for_status()
        tracks = res.json().get("data", [])
        filtered = [t for t in tracks if mood.lower() in t["title"].lower()]
        return [{"title": t["title"], "artist": t["user"]["name"], "url": t["permalink"]} for t in filtered[:10]]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
