from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import spotify_routes, auth_routes
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

app = FastAPI()
app.include_router(spotify_routes.router)
app.include_router(auth_routes.router)

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


@app.get("/")
def read_root():
    """ Placeholder """
    return {"message": "hello from backend"}


@app.get("/health")
def health_check():
    """ Basic health check function. """
    #TODO: add more functionality
    return {"status": "ok"}