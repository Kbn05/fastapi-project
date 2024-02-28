from pydantic import BaseModel
from typing import Optional
from .post import ResponsePost

# Create a Pydantic model to use as a request body

class Location(BaseModel):
    latitude: str
    longitude: str

class ResponseLocation(BaseModel):
    id: int
    latitude: float
    longitude: float
    distance: float
    post: Optional[ResponsePost]
