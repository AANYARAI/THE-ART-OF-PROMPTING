from pydantic import BaseModel


# Signup request
class UserCreate(BaseModel):
    email: str
    password: str


# Login request
class UserLogin(BaseModel):
    email: str
    password: str


# Response schema
class User(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True