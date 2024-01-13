from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint

app = FastAPI()

my_posts = [{"title": "Hello World", "content": "This is my first post", "id": 1},
            {"title": "Second Post", "content": "This is my second post", "id": 2},
            {"title": "Third Post", "content": "This is my third post", "id": 3},
            {"title": "Fourth Post", "content": "This is my fourth post", "id": 4}]
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
async def post(id: int, response: Response):
    for post in my_posts:
        if post['id'] == id:
            return {"data": post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"data": f"Post not found: {response.status_code}"}
        raise HTTPException(status_code=404, detail="Post not found")

# Create a route to handle POST requests sent to the /newpost path


@app.post("/newpost", status_code=status.HTTP_201_CREATED)
async def newpost(post: Post):
    print(post)
    postD = post.model_dump()
    postD['id'] = randint(1, 10000)
    my_posts.append(postD)
    return {"data": f"Post {post.title} created successfully"}

# Create a route to handle DELETE requests sent to the /posts/{id} path


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            my_posts.remove(post)
    raise HTTPException(status_code=404, detail="Post not found")

# Create a route to handle PUT requests sent to the /posts/{id} path


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, post_a: Post):
    for post in my_posts:
        if post['id'] == id:
            post['title'] = post_a.title
            post['content'] = post_a.content
            post['published'] = post_a.published
            post['likes'] = post_a.likes
            return {"data": post}
    raise HTTPException(status_code=404, detail="Post not found")
