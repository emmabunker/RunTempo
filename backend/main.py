from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from data.songs import SONG_DATABASE
from services.playlist import get_matching_tracks
from services.bpm import get_bpm_for_track
import os
import secrets
from urllib.parse import urlencode
from dotenv import load_dotenv
import base64
import requests

load_dotenv(dotenv_path=".env")
app = FastAPI()
spotify_access_token = None

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
    global spotify_access_token
    spotify_access_token = access_token

    return RedirectResponse("http://localhost:5173")

@app.get("/spotify/top-tracks")
def get_spotify_top_tracks():
    if not spotify_access_token:
        return {"error": "Not connected to Spotify"}
    
    response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks",
        headers={"Authorization": f"Bearer {spotify_access_token}"},
    )

    profile_data = response.json()

    tracks = []
    for track in profile_data.get("items", [])[:5]:
        artist_list = track.get("artists", [])
        artist_names = [artist["name"] for artist in artist_list] if artist_list else ["Unknown"]
        bpm = get_bpm_for_track(track["name"], artist_names)

        tracks.append({
            "title": track["name"],
            "artist": artist_names,
            "bpm": bpm
        })

    if not tracks:
        return {"message": "No tracks found"}
    
    return{"tracks": tracks}


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

@app.post("/spotify/generate-playlist")
def generate_spotify_playlist(request: PlaylistRequest):
    if not spotify_access_token:
        return {"error": "Not connected to Spotify"}
    
    response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks",
        headers={"Authorization": f"Bearer {spotify_access_token}"},
    )

    profile_data = response.json()

    tracks = []
    for track in profile_data.get("items", [])[:5]:
        artist_list = track.get("artists", [])
        artist_names = [artist["name"] for artist in artist_list] if artist_list else ["Unknown"]
        bpm = get_bpm_for_track(track["name"], artist_names)

        tracks.append({
            "title": track["name"],
            "artist": artist_names,
            "bpm": bpm
        })

    if not tracks:
        return {"message": "No tracks found"}
    
    matched_tracks = get_matching_tracks(tracks, request.target_bpm)

    return {
        "target_bpm": request.target_bpm,
        "tracks": matched_tracks,
    }