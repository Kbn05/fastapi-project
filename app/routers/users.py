from fastapi import APIRouter, HTTPException, status
from database.conn import cursor, mydbConnect
from app.schema.user import CreateUser, ResponseUser
from .. import utils

router = APIRouter(
    tags=["users"]
)

# Create a route to handle GET requests sent to the /users/{username} path


@router.get("/users/{username}", response_model=ResponseUser)
async def user(username: str):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        user_dict = dict(zip(cursor.column_names, user))
        return user_dict

    raise HTTPException(status_code=404, detail="No users found")


# Create a route to handle POST requests sent to the /users path


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def newuser(user: CreateUser):
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                   (user.username, user.email, utils.hash_password(user.password)))
    mydbConnect.commit()
    if cursor.rowcount < 1:
        raise HTTPException(status_code=404, detail="User not created")
    response_data = {"id": cursor.lastrowid, "username": user.username,
                     "email": user.email, "created_at": user.created_at}
    return ResponseUser(**response_data)
