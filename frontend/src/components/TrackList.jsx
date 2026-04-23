function TrackList({ tracks }) {
    if (tracks.length === 0) {
        return null;
    }

    return (
        <div style={{ marginTop: "1rem" }}>
            <h2>Suggested Tracks:</h2>
            <ul>
                {tracks.map((track, index) => (
                    <li key={index}>
                        {track.title} - {track.artist} ({track.bpm} BPM)
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default TrackList