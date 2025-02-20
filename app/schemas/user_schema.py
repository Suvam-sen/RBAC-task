from pydantic import BaseModel, EmailStr


class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "User"  # Default role is "User"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str