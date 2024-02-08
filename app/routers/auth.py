from fastapi import Response, status, HTTPException, APIRouter, Depends
from database.conn import cursor, mydbConnect
from app.schema.user import LoginUser
from app.schema.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from .. import utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
async def login(auth: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("SELECT username, email, password, id FROM users WHERE username = %s OR email = %s",
                   (auth.username, auth.username))
    user = cursor.fetchone()
    if user:
        if utils.verify_password(auth.password, user[2]):
            userStr = str(user[3])
            token = oauth2.create_access_token(
                data={"sub": userStr})
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=403, detail="Invalid username or password")
    raise HTTPException(status_code=403, detail="Invalid username or password")
