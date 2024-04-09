import logging

from fastapi import APIRouter, HTTPException
from concurrent.futures import ProcessPoolExecutor

import src.camera_component as cameraComponent
from multiprocessing import Process

logger = logging.getLogger(__name__)
executor = ProcessPoolExecutor(max_workers=2)
router = APIRouter(
    tags = ["router"],
    responses = {
        200: {"description": "ok"},
        404: {"description": "not found"}
    },
)
process = None

# 시작 API
@router.post("/camera")
async def startApp():
    global process
    # camera_component의 main 함수를 별도의 프로세스로 실행
    process = Process(target=cameraComponent.main)
    process.start()  # 프로세스 시작
    return {"message": "Camera processing started."}

# 종료 API
@router.post("/camera/end")
async def end():
    global process
    process.terminate()
    return {"message": "Camera is stopped."}