import requests

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

        artist_list = track.get("artists", [])
        artist_names = [artist["name"] for artist in artist_list] if artist_list else ["Unknown"]
        tracks.append({
            "title": track["name"],
            "artists": artist_names
        })

    return tracks
    