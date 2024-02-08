from pydantic import BaseModel
from typing import Optional

# Create a Pydantic model to use as a response body


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
