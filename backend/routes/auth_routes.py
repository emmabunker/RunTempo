from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from services import auth_state
import os
import secrets
from urllib.parse import urlencode
import base64
import requests

router = APIRouter(prefix="/auth/spotify")

@router.get("/login")
def spotify_login():
    """ Endpoint for handling Spotify login. """
    state = secrets.token_urlsafe(16)

    scopes = [
        "user-top-read", 
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-library-read",
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

@router.get("/callback")
def spotify_callback(code: str, state: str):
    """ Endpoint for handling callback to frontend after Spotify login. """
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
    auth_state.spotify_access_token = access_token

    return RedirectResponse("http://localhost:5173")