import json

from typing import Union
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


@app.get("/tracks", response_model=list[Track])
async def get_tracks():
    return app.state.tracks


@app.get("/tracks/{track_id}", response_model=Track)
async def get_track(track_id: int):
    for trk in app.state.tracks:
        if trk.id == track_id:
            return trk
    return Response("Track not found", status_code=404)


@app.post("/tracks", response_model=Track)
async def create_track(track: Track):
    track.id = max([trk.id for trk in app.state.tracks]) + 1
    app.state.tracks.append(track)
    return track


@app.put("/tracks/{track_id}", response_model=Track)
async def update_track(track_id: int, track: Track):
    for trk in app.state.tracks:
        if trk.id == track_id:
            trk.title = track.title
            trk.artist = track.artist
            trk.duration = track.duration
            trk.last_play = track.last_play
            return trk
    return Response("Track not found", status_code=404)


@app.delete("/tracks/{track_id}")
async def delete_track(track_id: int):
    for trk in app.state.tracks:
        if trk.id == track_id:
            app.state.tracks.remove(trk)
            return Response("Track deleted", status_code=200)
    return Response("Track not found", status_code=404)
