from fastapi import APIRouter, HTTPException, Depends, Response, status
from app.models.user_model import UserModel
from app.schemas.user_schema import LoginSchema, RegisterSchema
from app.database.db import get_db
from app.utils.security import hash_password, verify_password, create_access_token
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase


auth_router = APIRouter()

@auth_router.post("/register")
async def register(user: RegisterSchema, db: AsyncIOMotorDatabase = Depends(get_db)): #  Inject DB dynamically

    users_collection = db["users"]  #  Access users collection dynamically

    #  Check if email already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    hashed_password = hash_password(user.password)
    
    #  Convert schema to database model
    user_data = UserModel(
        username = user.username, 
        email = user.email, 
        password = hashed_password, 
        role = user.role or "User")

    await users_collection.insert_one(user_data.model_dump())
    return {
        "status": "success",
        "message": "User registered successfully",
        "data": user_data.model_dump()
    }



@auth_router.post("/login")
async def login(user_data: LoginSchema, response: Response, db: AsyncIOMotorDatabase = Depends(get_db)):

    users_collection = db["users"]

    db_user = await users_collection.find_one({"email": user_data.email})
    if not db_user or not verify_password(user_data.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create token payload
    payload = {"user_id": str(db_user["_id"]), "role": db_user["role"]}
    token = create_access_token(payload)
    
     # Set token in HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="strict",
        secure=False,
        max_age=3600,
    )


    return{
        "status": "success",
        "message": "User logged in successfully",
        "token": token,   # only for testing purposes
    }


@auth_router.get("/logout")
async def logout(response: Response):
    
    response.delete_cookie(
        key="access_token", 
        httponly=True, 
        samesite="strict", 
        secure=False
        )
    return JSONResponse(
        content={
            "status": "success", 
            "message": "User logged out successfully"
         },
        status_code=status.HTTP_200_OK
    )