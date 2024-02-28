from fastapi import Response, status, HTTPException, APIRouter, Depends
from database.conn import cursor, mydbConnect
from app.schema.post import CreatePost, ResponsePost
from .. import oauth2

router = APIRouter(
    tags=["posts"]
)

# Create a route to handle GET requests sent to the /posts path


@router.get("/posts", response_model=list[ResponsePost])
async def posts(limit: int = 10, token: int = Depends(oauth2.get_current_user), search: str = ""):
    cursor.execute(
        "SELECT posts.*, users.id, users.username, users.email, users.created_at FROM posts INNER JOIN users ON posts.author_id = users.id WHERE posts.content LIKE %s ORDER BY users.created_at DESC LIMIT %s", ('%' + search + '%', limit,))
    my_posts = cursor.fetchall()
    post_list = []
    if my_posts:
        for post in my_posts:
            post_dict = {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "published": post[3],
                "likes": post[4],
                "created_at": post[5],
                "author": {
                    "id": post[7],
                    "username": post[8],
                    "email": post[9],
                    "created_at": post[10]
                }
            }
            post_list.append(post_dict)
        return post_list

    raise HTTPException(status_code=404, detail="No posts found")

# Create a route to handle GET requests sent to the /posts/{id} path


@router.get("/posts/{id}", response_model=ResponsePost)
async def post(id: int, response: Response):
    cursor.execute("SELECT posts.*, users.id, users.username, users.email, users.created_at FROM posts INNER JOIN users ON posts.author_id = users.id WHERE posts.id = %s", (id,))
    my_posts = cursor.fetchone()
    print(my_posts[0])
    if my_posts:
        post_dict = {
            "id": my_posts[0],
            "title": my_posts[1],
            "content": my_posts[2],
            "published": my_posts[3],
            "likes": my_posts[4],
            "created_at": my_posts[5],
            "author": {
                "id": my_posts[7],
                "username": my_posts[8],
                "email": my_posts[9],
                "created_at": my_posts[10]
            }
        }
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
    cursor.execute("INSERT INTO posts (title, content, published, likes, author_id) VALUES (%s, %s, %s, %s, %s)",
                   (post.title, post.content, post.published, post.likes, token[2]))
    mydbConnect.commit()
    post_id = cursor.lastrowid
    response_data = {"id": post_id, "title": post.title,
                     "content": post.content, "likes": int(post.likes), "author": {"id": token[2], "username": token[0], "email": token[1], "created_at": token[3]}}
    return ResponsePost(**response_data)
    # return f"Post {post.title} created successfully"

# Create a route to handle DELETE requests sent to the /posts/{id} path


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, token: int = Depends(oauth2.get_current_user)):
    cursor.execute("SELECT author_id FROM posts WHERE id = %s", (id,))
    my_posts = cursor.fetchone()
    if my_posts:
        post_dict = dict(zip(cursor.column_names, my_posts))
        if post_dict['author_id'] != token[2]:
            raise HTTPException(
                status_code=403, detail="You are not authorized to delete this post")
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Post not found")

# Create a route to handle PUT requests sent to the /posts/{id} path


@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ResponsePost)
async def update_post(id: int, post_a: CreatePost, token: int = Depends(oauth2.get_current_user)):
    cursor.execute("SELECT author_id FROM posts WHERE id = %s", (id,))
    my_posts = cursor.fetchone()
    if my_posts:
        post_dict = dict(zip(cursor.column_names, my_posts))
        if post_dict['author_id'] != token[2]:
            raise HTTPException(
                status_code=403, detail="You are not authorized to update this post")
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s, likes = %s, author_id = %s WHERE id = %s", (
        post_a.title, post_a.content, post_a.published, post_a.likes, token[2], id))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="Post not found")
    post_id = cursor.lastrowid
    response_data = {"id": id, "title": post_a.title,
                     "content": post_a.content, "likes": int(post_a.likes), "author": {"id": token[2], "username": token[0], "email": token[1], "created_at": token[3]}}
    return ResponsePost(**response_data)

@router.get("/posts/{id}/likes", status_code=status.HTTP_202_ACCEPTED)
async def like_post(id: int, token: int = Depends(oauth2.get_current_user)):
    cursor.execute("SELECT id FROM posts WHERE id = %s", (id,))
    post_exists = cursor.fetchone()

    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")

    cursor.execute("SELECT posts.id AS post_id, COUNT(likes.user_id) AS total_likes, GROUP_CONCAT(users.username SEPARATOR ', ') AS liked_by FROM posts LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN users ON likes.user_id = users.id WHERE posts.id = %s GROUP BY posts.id", (id,))
    like_data = cursor.fetchone()

    if like_data:
        if like_data[2] is not None:
            return {
                "post_id": like_data[0],
                "total_likes": like_data[1],
                "liked_by": like_data[2]
            }
        else:
            return {"post_id": like_data[0], "total_likes": 0, "liked_by": ""}
    else:
        return {"post_id": id, "total_likes": 0, "liked_by": ""}

@router.post("/posts/{id}/likes", status_code=status.HTTP_201_CREATED)
async def like_post(id: int, token: int = Depends(oauth2.get_current_user)):
    cursor.execute("SELECT id FROM posts WHERE id = %s", (id,))
    post_exists = cursor.fetchone()

    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")

    cursor.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s", (id, token[2]))
    like_exists = cursor.fetchone()

    if like_exists:
        cursor.execute("DELETE FROM likes WHERE post_id = %s AND user_id = %s", (id, token[2]))
        mydbConnect.commit()
        return {"message": "Post unliked successfully"}

    cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s)", (id, token[2]))
    mydbConnect.commit()
    return {"message": "Post liked successfully"}