from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# json template
# {"id": "1", "title": "Free", "artist": "Ultra Nate", "duration": "220", "last_play": "2018-05-17 16:56:21"}
class Track(BaseModel):
    id: int = None
    title: str
    artist: str
    duration: float
    last_play: datetime
