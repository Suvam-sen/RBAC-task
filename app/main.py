from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import auth_router
from app.routes.course_routes import course_router
# from app.utils.database import connect_db


app = FastAPI()


# @app.on_event("startup")
# async def startup_db():
#     await connect_db()


origins = [
    "http://127.0.0.1:8000" 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers", "Content-Type", "Authorization", "Access-Control-Allow-Origin","Set-Cookie"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(course_router, prefix="/courses", tags=["Courses"])