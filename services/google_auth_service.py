from auth.security.oauth_google import _oauth_google
from fastapi import Request
from fastapi import HTTPException
from auth.db.mongodb import user_collection

from auth.services.auth_service import (
    create_access_token,create_refresh_token,store_refresh_token
)


async def google_login(request: Request):
    
    redirect_url = request.url_for("google_callback")

    return await _oauth_google.google.authorize_redirect(
        request,
        redirect_url
    )

async def google_callback(request: Request):

    try:
        token = await _oauth_google.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(
            status_code= 401,
            detail="Google Auth Failed"
        )

    user_info = token["userinfo"]

    email = user_info.get("email")
    google_id = user_info.get("sub")
    full_name = user_info.get("name","")

    existing_user = user_collection.find_one({
        "email" : email
    })

    if existing_user and existing_user["provider"] == "local":
        raise HTTPException(
            status_code=400,
            detail="This email is already registered with email-password"
        )

    if existing_user is None:

        # to ensure that duplicate usernames dont come up
        base_username = email.split("@")[0]
        username = base_username

        counter = 1

        while user_collection.find_one({"username": username}):
            username = f"{base_username}{counter}"
            counter += 1

        user_collection.insert_one({
        "username": username,
        "email": email,
        "full_name": full_name,
        "provider": "google",
        "google_id": google_id,
        "hashed_password": None,
        "disabled": False,
        "failed_attempts": 0,
        "locked_until": None
        })

    user = user_collection.find_one(
        {"email": email}
    )

    access_token = create_access_token({
        "sub": user["email"]
    })

    refresh_token = create_refresh_token()

    store_refresh_token(
        user["email"],
        refresh_token
    )

    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
}