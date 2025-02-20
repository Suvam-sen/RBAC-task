from fastapi import APIRouter, HTTPException, Depends
from app.database.db import get_db
from app.schemas.course_schema import CourseSchema
from app.middleware.auth_middleware import admin_required
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


course_router = APIRouter()

@course_router.post("/", dependencies= [Depends(admin_required)], summary="Create a new course (Admin Only)")
async def create_course(course: CourseSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
    
    course_dict = course.model_dump()
    course_collection = db["courses"]  # accesing db dynamically

    result = await course_collection.insert_one(course_dict)

    created_course = await course_collection.find_one(
        {"_id": result.inserted_id},
        {"_id": 0}  # Exclude _id
    )
    return {
        "status": "success",
        "message": "Course created",
        "data": created_course
    }


@course_router.put("/{course_id}", dependencies= [Depends(admin_required)], summary="Update course (Admin Only)")
async def update_course(course_id: str, course: CourseSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
    course_collection = db["courses"]  # accesing db dynamically
    result = await course_collection.update_one(
        {"_id": ObjectId(course_id)},
        {
            "$set": course.model_dump()
        }
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404,detail= "Course not found")
    return {
        "status": "success",
        "message": "Course updated"
    }


@course_router.delete("/{course_id}", dependencies= [Depends(admin_required)], summary="Delete course (Admin Only)")
async def delete_course(course_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    course_collection = db["courses"]  # accesing db dynamically
    result = await course_collection.delete_one({"_id": ObjectId(course_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return {
        "status": "success",
        "message": "Course deleted successfully"
        }


@course_router.get("/")
async def get_all_courses(db: AsyncIOMotorDatabase = Depends(get_db)):
    course_collection = db["courses"]  # accesing db dynamically
    
    courses = await course_collection.find({}, {"_id": 0}).to_list(100)

    return {
        "status": "success",
        "message": "Courses retrieved successfully",
        "data": courses
    }


@course_router.get("/{course_id}")
async def get_course(course_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    course_collection = db["courses"]  # accesing db dynamically
    course = await course_collection.find_one({"_id": ObjectId(course_id)}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course