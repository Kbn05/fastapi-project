from jose import JWTError, jwt
from app.schema.token import TokenData
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database.conn import cursor, mydbConnect

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "052f77666c63cd29e12f9fd2d71c26735bb190d28143b997b812659e4be890db"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    to_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": to_expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
        return token_data
    except JWTError as e:
        print(e)
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    userId = verify_access_token(token, credentials_exception)
    cursor.execute(
        "SELECT username, email, id, created_at FROM users WHERE id = %s", (userId.id,))
    session = cursor.fetchone()

    return session
