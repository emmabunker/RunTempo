def get_matching_tracks(song_database, target_bpm, limit=3):
    sorted_tracks = sorted(
        song_database,
        key=lambda track: abs(track["bpm"] - target_bpm)
    )

    matched_tracks = sorted_tracks[:limit]
    return matched_tracks