from fastapi import APIRouter,HTTPException
from auth.schemas.user import User,UserCreate, UserLogin
from auth.schemas.token import RefreshTokenRequest,LogoutRequest
from auth.services.auth_service import register_user
from auth.services.auth_service import authenticate_user
from auth.services.auth_service import create_access_token
from fastapi import Depends, HTTPException
from auth.services.auth_service import get_current_user
from auth.services.auth_service import oauth2_scheme
from auth.services.auth_service import create_refresh_token,store_refresh_token

from auth.services.auth_service import validate_refresh_token,delete_refresh_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=User
)
async def register_function(
    user: UserCreate
):
    return register_user(user)


@router.post("/login")
async def login(user: UserLogin):
    authenticated_user = authenticate_user(user.email, user.password)
    
    if not authenticated_user:
        raise HTTPException(
            status_code= 401,
            detail = "Invalid Credentials"
        )

    access_token = create_access_token({
        "sub": authenticated_user["email"]
    })

    refresh_token = create_refresh_token()

    store_refresh_token(
        authenticated_user["email"],
        refresh_token
    )

    return {
        "access_token" : access_token,
        "refresh_token": refresh_token,
        "token_type" : "bearer"
    }


@router.get("/me", response_model=User)
async def read_me(token: str = Depends(oauth2_scheme)):

    user = get_current_user(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return user


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    validated_token = validate_refresh_token(
    request.refresh_token
)
    
    if not validated_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    # email = validated_token["email"]

    email = validated_token["email"]

    delete_refresh_token(request.refresh_token)

    new_access_token = create_access_token({
        "sub" : email
    })

    new_refresh_token = create_refresh_token()

    store_refresh_token(email,new_refresh_token)

    return {
    "access_token": new_access_token,
    "refresh_token": new_refresh_token,
    "token_type": "bearer"
}

@router.post("/logout")
async def logout(request: LogoutRequest):

    delete_refresh_token(request.refresh_token)

    return{
        "message" : "Logged Out Successfully"
    }