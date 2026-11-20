from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str = "Legal Professional"
    role: str = "Senior Analyst"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str
