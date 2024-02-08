from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Create a Pydantic model to use as a request body


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()


class CreateUser(User):
    pass


class LoginUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str


# Create a Pydantic model to use as a response body


class ResponseUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True
