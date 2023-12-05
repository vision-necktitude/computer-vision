from fastapi import FastAPI
import subprocess
import os

app = FastAPI()
process = None

# 시작 API
@app.get("/init")
async def init():
    # main.py 파일이 있는 디렉토리로 이동
    directory_path = "src"
    os.chdir(directory_path)

    # main.py 실행
    process = subprocess.Popen(["python", "main.py"], shell=True)


# 종료 API
@app.get("/end")
async def end():
    if process is not None:
        process.kill()