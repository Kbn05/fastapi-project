from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint
import mysql.connector
import time

app = FastAPI()

# my_posts = [{"title": "Hello World", "content": "This is my first post", "id": 1},
#             {"title": "Second Post", "content": "This is my second post", "id": 2},
#             {"title": "Third Post", "content": "This is my third post", "id": 3},
#             {"title": "Fourth Post", "content": "This is my fourth post", "id": 4}]

while True:
    try:
        mydbConnect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Zot10175",
            database="fastapi"
        )
        cursor = mydbConnect.cursor()
        print("Connected to database")
        break
    except:
        print("Error connecting to database")
        time.sleep(5)

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
    cursor.execute("SELECT * FROM posts")
    my_posts = cursor.fetchall()
    return {"data": my_posts}

# Create a route to handle GET requests sent to the /posts/{id} path


@app.get("/posts/{id}")
async def post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    my_posts = cursor.fetchall()
    if len(my_posts) > 0:
        return {"data": my_posts}
    # for post in my_posts:
    #     if post['id'] == id:
    #         return {"data": post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"data": f"Post not found: {response.status_code}"}
    raise HTTPException(status_code=404, detail="Post not found")

# Create a route to handle POST requests sent to the /newpost path


@app.post("/newpost", status_code=status.HTTP_201_CREATED)
async def newpost(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published, likes) VALUES (%s, %s, %s, %s)",
                   (post.title, post.content, post.published, post.likes))
    mydbConnect.commit()
    return {"data": f"Post {post.title} created successfully"}

# Create a route to handle DELETE requests sent to the /posts/{id} path


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Post not found")

# Create a route to handle PUT requests sent to the /posts/{id} path


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, post_a: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s, likes = %s WHERE id = %s", (
        post_a.title, post_a.content, post_a.published, post_a.likes, id))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Post not found")
