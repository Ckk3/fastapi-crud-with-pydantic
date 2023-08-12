import json


from fastapi import FastAPI, Response
from models import Track

app = FastAPI(debug=True)

@app.on_event("startup")
async def startup_event():
    datapath = "data/tracks.json"
    with open(datapath, "r") as f:
        data = json.load(f)
    
    app.state.tracks = [Track(**track) for track in data]


@app.get("/")
async def root():
    return Response("Welcome to the music API!", status_code=200)


@app.get("/tracks")
async def get_tracks():
    return app.state.tracks