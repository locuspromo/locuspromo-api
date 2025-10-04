from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    res = requests.get(f"{AUDIUS_API}/tracks/trending", params={"app_name": "locuspromo"})
    tracks = res.json().get("data", [])
    filtered = [t for t in tracks if mood.lower() in t["title"].lower()]
    return [{"title": t["title"], "artist": t["user"]["name"], "url": t["permalink"]} for t in filtered[:10]]
