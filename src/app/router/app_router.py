import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter(
    tags = ["router"],
    responses={404: {"description": "not found"}, 200: {"description": "ok"}},
)

# 시작 API
@router.post("/init")
async def initApp():
    print("##")


# 종료 API
@router.post("/end")
async def end():
    print("@@")