import requests
from services.bpm import get_bpm_for_track

def get_artist_names(track):
    artist_list = track.get("artists", [])
    artist_names = [artist["name"] for artist in artist_list] if artist_list else ["Unknown"]
    return artist_names


def get_user_playlists(access_token):
    response = requests.get(
        "https://api.spotify.com/v1/me/playlists",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    data = response.json()

    playlists = []

    for playlist in data.get("items", []):
        playlists.append({
            "id": playlist["id"],
            "name": playlist["name"],
            "track_count": playlist["tracks"]["total"],
        })

    return playlists

def get_playlist_tracks(access_token, playlist_id):
    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    data = response.json()
    tracks = []

    for item in data.get("items", []):
        track = item.get("track")
        if not track:
            continue

        artist_names = get_artist_names(track)
        tracks.append({
            "title": track["name"],
            "artist": artist_names
        })

    return tracks

def get_top_tracks(access_token):
    response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    profile_data = response.json()
    tracks = []

    for track in profile_data.get("items", [])[:5]:
        artist_names = get_artist_names(track)

        tracks.append({
            "title": track["name"],
            "artist": artist_names
        })
        
    if not tracks:
            return {"message": "No tracks found"}
    
    tracks = add_bpm_to_tracks(tracks)
    
    return tracks

def add_bpm_to_tracks(tracks):
    track_list = []

    for track in tracks:
        title = track["title"]
        artist_names = track["artist"]
        bpm = get_bpm_for_track(title, artist_names)

        track_list.append({
            "title": title,
            "artist": artist_names,
            "bpm": bpm
        })
        
    return track_list
    