from fastapi import FastAPI,HTTPException,status
from auth.api.endpoints.test import router as test_router
from auth.api.endpoints.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from auth.config import SECRET_KEY


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

app.include_router(test_router,prefix="/api")
app.include_router(auth_router)