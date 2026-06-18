from fastapi import APIRouter
from auth.db.test_model import User_Info as user

router = APIRouter()

@router.get("/status")
async def get_status():
    return {
        "status": "working"
    }

@router.get("/high-traffic")
async def high_load():
    return {
        "status" : "down due to high traffic"
    }