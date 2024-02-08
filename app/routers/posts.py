from fastapi import Response, status, HTTPException, APIRouter, Depends
from database.conn import cursor, mydbConnect
from app.schema.post import CreatePost, ResponsePost
from .. import oauth2

router = APIRouter(
    tags=["posts"]
)

# Create a route to handle GET requests sent to the /posts path


@router.get("/posts", response_model=list[ResponsePost])
async def posts():
    cursor.execute("SELECT * FROM posts")
    my_posts = cursor.fetchall()
    post_list = []
    if my_posts:
        for post in my_posts:
            post_dict = dict(zip(cursor.column_names, post))
            post_list.append(post_dict)
        return post_list

    raise HTTPException(status_code=404, detail="No posts found")

# Create a route to handle GET requests sent to the /posts/{id} path


@router.get("/posts/{id}", response_model=ResponsePost)
async def post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    my_posts = cursor.fetchone()
    if my_posts:
        post_dict = dict(zip(cursor.column_names, my_posts))
        return post_dict
    # for post in my_posts:
    #     if post['id'] == id:
    #         return {"data": post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"data": f"Post not found: {response.status_code}"}
    raise HTTPException(status_code=404, detail="Post not found")

# Create a route to handle POST requests sent to the /newpost path


@router.post("/newpost", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
async def newpost(post: CreatePost, token: int = Depends(oauth2.get_current_user)):
    cursor.execute("INSERT INTO posts (title, content, published, likes) VALUES (%s, %s, %s, %s)",
                   (post.title, post.content, post.published, post.likes))
    mydbConnect.commit()
    post_id = cursor.lastrowid
    response_data = {"id": post_id, "title": post.title,
                     "content": post.content, "likes": int(post.likes)}
    return ResponsePost(**response_data)
    # return f"Post {post.title} created successfully"

# Create a route to handle DELETE requests sent to the /posts/{id} path


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, token: int = Depends(oauth2.get_current_user)):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Post not found")

# Create a route to handle PUT requests sent to the /posts/{id} path


@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ResponsePost)
async def update_post(id: int, post_a: CreatePost, token: int = Depends(oauth2.get_current_user)):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s, likes = %s WHERE id = %s", (
        post_a.title, post_a.content, post_a.published, post_a.likes, id))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Post not found")
    post_id = cursor.lastrowid
    response_data = {"id": id, "title": post_a.title,
                     "content": post_a.content, "likes": int(post_a.likes)}
    return ResponsePost(**response_data)
