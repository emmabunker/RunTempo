from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from data.songs import SONG_DATABASE
from services.playlist import get_matching_tracks
import os
import secrets
from urllib.parse import urlencode
from dotenv import load_dotenv
import base64
import requests

load_dotenv(dotenv_path=".env")
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/auth/spotify/login")
def spotify_login():
    state = secrets.token_urlsafe(16)

    scopes = [
        "user-top-read", 
        "playlist-modify-public",
        "playlist-modify-private",
    ]

    query_params = {
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "scope": " ".join(scopes),
        "state": state,
    }

    auth_url = "https://accounts.spotify.com/authorize?" + urlencode(query_params)

    return RedirectResponse(auth_url)

@app.get("/auth/spotify/callback")
def spotify_callback(code: str, state: str):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    token_url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json()
    access_token = token_data.get("access_token")

    profile_response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    profile_data = profile_response.json()
    with open("output.json", "w") as f:
        print(profile_data, file=f)

    items = profile_data.get("items", [])

    if not items:
        return {"message": "No tracks found"}

    first_track = items[0]
    track_name = first_track.get("name")
    artist_list = first_track.get("artists", [])
    artist_name = artist_list[0]["name"] if artist_list else "Unknown"

    return {
    "message": "Spotify auth complete",
    "track_name": track_name,
    "track_artist": artist_name,
    "has_access_token": access_token is not None,
}

class PlaylistRequest(BaseModel):
    target_bpm: int = Field(..., ge=60, le=220)


@app.get("/")
def read_root():
    return {"message": "hello from backend"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate-playlist")
def generate_playlist(request: PlaylistRequest):
    matched_tracks = get_matching_tracks(SONG_DATABASE, request.target_bpm)

    return {
        "target_bpm": request.target_bpm,
        "tracks": matched_tracks,
    }