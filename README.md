# RunTempo

RunTempo is a full-stack web app that generates running playlists based on a target running cadence in BPM (beats per minute). Users can input a desired tempo, and the app returns songs that best match that pace.

## Features

- Input target BPM
- Backend matching algorithm to find closest songs
- Dynamic frontend rendering of playlist results
- Input validation (frontend + backend)
- Modular backend structure (routes, services, data)

## Tech Stack

**Frontend**
- React (Vite)
- JavaScript

**Backend**
- Python
- FastAPI

## How It Works

1. User enters a target BPM in the frontend
2. Frontend sends a POST request to the backend
3. Backend:
   - Validates the input
   - Compares BPM against a dataset
   - Sorts songs by closeness to target BPM
4. Backend returns matching songs
5. Frontend displays the results

## Project Structure
RunTempo/
backend/
main.py
data/
songs.py
services/
playlist.py
frontend/
src/
components/
TrackList.jsx
App.jsx


## Running Locally
### Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm run dev

## Future Improvements
Spotify integration (auth + playlist creation)
Real BPM data integration
Improved recommendation algorithm
UI/UX improvements
Deployment (AWS)

## Author
Emma Bunker
