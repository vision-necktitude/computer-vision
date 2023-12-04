from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

@app.get("/init")
async def init():
    # main.py 파일이 있는 디렉토리로 이동
    directory_path = "src"
    os.chdir(directory_path)

    # main.py 실행
    subprocess.run(["python", "main.py"], shell=True)
