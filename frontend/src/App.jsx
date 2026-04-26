import { useState, useEffect } from "react";
import TrackList from "./components/TrackList";

function App() {
  const [targetBpm, setTargetBpm] = useState("");
  const [tracks, setTracks] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylistId, setSelectedPlaylistId] = useState("");
  const [playlistTracks, setPlaylistTracks] = useState([]);

  useEffect(() => {
  if (!selectedPlaylistId) {
    return;
  }

  async function fetchTracks() {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/spotify/playlists/${selectedPlaylistId}/tracks`
      );

      const data = await response.json();
      console.log("Playlist tracks:", data);

      setPlaylistTracks(data.playlist_tracks);
    } catch (error) {
      console.error(error);
    }
  }

  fetchTracks();
}, [selectedPlaylistId]);


  const handleGenerate = async () => {
    setErrorMessage("");
    setTracks([]);

    const bpmNumber = Number(targetBpm);

    if (!targetBpm || bpmNumber < 60 || bpmNumber > 220) {
      setErrorMessage("Please enter a BPM between 60 and 220.");
      return;
    }

    if (!selectedPlaylistId) {
      setErrorMessage("Please select a playlist first.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/spotify/generate-playlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          target_bpm: Number(targetBpm),
          playlist_id: selectedPlaylistId,
        }),
      });

      if (!response.ok) {
        setErrorMessage("The backend rejected that BPM.");
        return;
      }

      const data = await response.json();
      setTracks(data.tracks);
    } catch (error) {
      console.error(error);
      setTracks([]);
    }
  };

  const handleLoadSpotifyTracks = async () => {
    setErrorMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/spotify/top-tracks");
      const data = await response.json();

      setTracks(data.tracks)
    } catch (error) {
      console.error(error);
      setErrorMessage("Could not load Spotify tracks.");
    }
  };

  const handleLoadPlaylists = async () => {
    setErrorMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/spotify/playlists");
      const data = await response.json();

      console.log(data);
      setPlaylists(data.playlists);
    } catch (error) {
      console.error(error);
      setErrorMessage("Could not load Spotify playlists.");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>RunTempo</h1>
      <p>Generate a running playlist based on your target tempo.</p>
      
      <button
        onClick={() => {
          window.location.href = "http://127.0.0.1:8000/auth/spotify/login";
        }}
        style={{ padding: "0.5rem 1rem", marginBottom: "1rem" }}
      >
        Connect Spotify
      </button>

      <br />

      <button
        onClick={handleLoadSpotifyTracks}
        style={{ padding: "0.5rem 1rem", marginBottom: "1rem" }}
      >
        Load My Top Tracks
      </button>
      
      <button 
        onClick={handleLoadPlaylists}
        style={{ padding: "0.5rem 1rem", marginBottom: "1rem" }}
      >
        Load My Playlists
      </button>

      <br />

      <select
        value={selectedPlaylistId}
        onChange={(e) => setSelectedPlaylistId(e.target.value)}
      >
        
        <option value="">Select a playlist</option>

        {playlists.map((playlist) => (
          <option key={playlist.id} value={playlist.id}>
            {playlist.name} ({playlist.track_count} tracks)
          </option>
        ))}
      </select>

      <br />

      <label htmlFor="bpm-input">Target BPM:</label>
      <br />
      <input
        id="bpm-input"
        type="number"
        value={targetBpm}
        onChange={(e) => setTargetBpm(e.target.value)}
        placeholder="Enter BPM"
        style={{ marginTop: "0.5rem", marginRight: "0.5rem", padding: "0.5rem" }}
      />

      <button onClick={handleGenerate} style={{ padding: "0.5rem 1rem" }}>
        Generate Playlist
      </button>

      {errorMessage && (
        <p style={{ marginTop: "1rem", color: "crimson" }}>{errorMessage}</p>
      )}

      <TrackList tracks={tracks} />
      <TrackList tracks={playlistTracks} />
    </div>
  );
}

export default App;