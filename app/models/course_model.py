from pydantic import BaseModel
from typing import Optional

class CourseModel(BaseModel):
    title: str
    description: Optional[str] = None
    instructor: str
    price: float