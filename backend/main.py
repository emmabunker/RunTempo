from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from data.songs import SONG_DATABASE
from services.playlist import get_matching_tracks

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