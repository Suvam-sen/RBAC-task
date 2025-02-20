from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = None
db = None

try:
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))



# Dependency function for FastAPI
async def get_db():
    return db