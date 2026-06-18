from fastapi import FastAPI,HTTPException,status
from auth.api.endpoints.test import router as test_router
from auth.api.endpoints.auth import router as auth_router


app = FastAPI()

app.include_router(test_router,prefix="/api")
app.include_router(auth_router)