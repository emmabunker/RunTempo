from fastapi import APIRouter
from services import auth_state
from services.playlist import get_matching_tracks
from services.spotify_integration import (
    get_user_playlists,
    get_playlist_tracks,
    get_top_tracks,
    add_bpm_to_tracks
)
from pydantic import BaseModel, Field

router = APIRouter(prefix="/spotify")

class PlaylistRequest(BaseModel):
    target_bpm: int = Field(..., ge=60, le=220)
    playlist_id: str

@router.get("/top-tracks")
def get_spotify_top_tracks():
    """ Endpoint for handling getting top tracks from Spotify. """
    if not auth_state.spotify_access_token:
        return {"error": "Not connected to Spotify"}
    
    tracks = get_top_tracks(auth_state.spotify_access_token)
    
    return{"tracks": tracks}

@router.get("/playlists")
def get_spotify_playlists():
    """ Endpoint for handling retrieval of Spotify playlists. """
    if not auth_state.spotify_access_token:
        return {"error": "Not connected to Spotify"}

    playlists = get_user_playlists(auth_state.spotify_access_token)

    return {"playlists": playlists}

@router.get("/playlists/{playlist_id}/tracks")
def get_spotify_playlist_tracks(playlist_id: str):
    if not auth_state.spotify_access_token:
        return {"error": "Not connected to Spotify"}

    playlist_tracks = get_playlist_tracks(auth_state.spotify_access_token, playlist_id)

    return {"playlist_tracks": playlist_tracks}

@router.post("/generate-playlist")
def generate_spotify_playlist(request: PlaylistRequest):
    """ Generates a playlist based on Spotify tracks. """
    if not auth_state.spotify_access_token:
        return {"error": "Not connected to Spotify"}
    
    tracks = get_playlist_tracks(auth_state.spotify_access_token, request.playlist_id)
    tracks_with_bpm = add_bpm_to_tracks(tracks)
    matched_tracks = get_matching_tracks(tracks_with_bpm, request.target_bpm)

    return {
        "target_bpm": request.target_bpm,
        "tracks": matched_tracks,
    }