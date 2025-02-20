from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "User"  # Default role is "User"
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
