import { useState } from "react";
import TrackList from "./components/TrackList";

function App() {
  const [targetBpm, setTargetBpm] = useState("");
  const [tracks, setTracks] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  const handleGenerate = async () => {
    setErrorMessage("");
    setTracks([]);

    const bpmNumber = Number(targetBpm);

    if (!targetBpm || bpmNumber < 60 || bpmNumber > 220) {
      setErrorMessage("Please enter a BPM between 60 and 220.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/generate-playlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          target_bpm: Number(targetBpm),
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

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>RunTempo</h1>
      <p>Generate a running playlist based on your target tempo.</p>

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
    </div>
  );
}

export default App;