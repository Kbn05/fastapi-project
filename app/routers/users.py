from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from database.conn import cursor, mydbConnect
from app.schema.user import CreateUser, ResponseUser, PutUser
from .. import utils, oauth2
from datetime import datetime

router = APIRouter(
    tags=["users"]
)

# Create a route to handle GET requests sent to the /users/{username} path


@router.get("/users/{username}", response_model=ResponseUser)
async def user(username: str):
    cursor.execute("SELECT id, username, email, created_at, career, age, image FROM users WHERE username = %s", (username,))
    users = cursor.fetchone()
    print(users)
    if users:
        response_data = {"id": users[0], "username": users[1],
                         "email": users[2], "created_at": users[3], "career": users[4], "age": users[5], "image": 'http://20.163.25.147:8000/static/' + users[6]}
        return ResponseUser(**response_data)
    raise HTTPException(status_code=404, detail="No users found")


# Create a route to handle POST requests sent to the /users path


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def newuser(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    career: str = Form(None),
    age: int = Form(None),
    file: UploadFile = File(...),
):
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    print(user)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    file.filename = f"{file.filename}"
    contentFile = await file.read()
    with open(f"app/static/{file.filename}", "wb") as image:
        image.write(contentFile)
    cursor.execute("INSERT INTO users (username, email, password, career, age, image) VALUES (%s, %s, %s, %s, %s, %s)",
                   (username, email, utils.hash_password(password), career, age, file.filename))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="User not created")
    response_data = {"id": cursor.lastrowid, "username": username,
                     "email": email, "created_at": str(datetime.now()),"career": career, "age": age, "image": 'http://20.163.25.147:8000/static/' + file.filename}
    return ResponseUser(**response_data)

# Create a route to handle PUT requests sent to the /users/{username} path

# Create a route to handle DELETE requests sent to the /users/{username} path
@router.delete("/users/{username}")
async def delete_user(username: str, token: int = Depends(oauth2.get_current_user),):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(user[0], token[2])
    if user[0] != token[2]:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Create a route to handle PUT requests sent to the /users/{username} path
@router.put("/users/{username}")
async def update_user(
    username: str, 
    new_username: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    career: str = Form(None),
    age: int = Form(None),
    file: UploadFile = File(None),
    token: int = Depends(oauth2.get_current_user)):
    if file:
        file.filename = f"{file.filename}"
        contentFile = await file.read()
        with open(f"app/static/{file.filename}", "wb") as image:
            image.write(contentFile)
        image = file.filename

    cursor.execute("SELECT id, username, email, password, career, age, image FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id[0] != token[2]:
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")
    cursor.execute("UPDATE users SET username = %s, email = %s, password = %s, career = %s, age = %s, image = %s WHERE username = %s",
                   (new_username or user_id[1], email or user_id[2], utils.hash_password(password) if password else user_id[3], career or user_id[4], age or user_id[5], file.filename if file else user_id[6],username))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="User not updated")
    return {"message": "User updated successfully"}
