from pydantic import BaseModel

class CourseSchema(BaseModel):
    title: str
    description: str
    instructor: str
    price: float
