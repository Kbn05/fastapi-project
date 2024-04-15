from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import ResponseUser

# Create a Pydantic model to use as a request body


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    likes: Optional[int] = 0
    created_at: datetime = datetime.now()
    image: Optional[str] = None


class CreatePost(Post):
    pass

# Create a Pydantic model to use as a response body


class ResponsePost(Post):
    id: int
    author: ResponseUser

    class Config:
        from_attributes = True
