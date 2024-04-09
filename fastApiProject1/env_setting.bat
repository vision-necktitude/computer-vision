@echo off

rem 가상환경 경로 (가상환경 폴더가 프로그램과 같은 경로에 있다고 가정)
set ENV_PATH= venv

rem 가상환경 활성화
call %ENV_PATH%/Scripts/activate

rem 프로그램 실행 (가상환경이 활성화된 상태에서 실행)
uvicorn src.app.fastApi:app --reload

rem 가상환경 비활성화 (프로그램 실행 후에는 권장)
deactivate