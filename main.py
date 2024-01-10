from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randint

app = FastAPI()

my_posts = [{"title": "Hello World", "content": "This is my first post", "id": 1}, {"title": "Second Post",
                                                                                    "content": "This is my second post", "id": 2}, {"title": "Third Post", "content": "This is my third post", "id": 3}]

# Create a Pydantic model to use as a request body


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    likes: Optional[int] = None

# Create a route to handle GET requests sent to the / path


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Create a route to handle GET requests sent to the /posts path


@app.get("/posts")
async def posts():
    return {"data": my_posts}

# Create a route to handle GET requests sent to the /posts/{id} path


@app.get("/posts/{id}")
async def post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return {"data": post}
    return {"data": "Post not found"}

# Create a route to handle POST requests sent to the /newpost path


@app.post("/newpost")
async def newpost(post: Post):
    print(post)
    postD = post.model_dump()
    postD['id'] = randint(1, 10000)
    my_posts.append(postD)
    return {"data": f"Post {post.title} created successfully"}
