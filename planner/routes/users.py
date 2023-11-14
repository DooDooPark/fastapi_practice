from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(
    tags=["User"],
)

users = {}

@user_router.post("/signup")
async def sign_new_user(data:User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User doesn't exist"
        )
    users[data.email] = data
    return{
        "message":"User successsfully registered!"
    }

@user_router.post("/signin")
async def sign_user_in(user:UserSignIn)->dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )

    return {
        "message":"User signed in success."
    }