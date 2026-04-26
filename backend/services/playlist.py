def get_matching_tracks(song_database, target_bpm, limit=3):
    tracks_with_bpm = [
        track for track in song_database
        if track.get("bpm") is not None
    ]
    sorted_tracks = sorted(
        tracks_with_bpm,
        key=lambda track: abs(track["bpm"] - target_bpm)
    )

    matched_tracks = sorted_tracks[:limit]
    return matched_tracks