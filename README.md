# Vision Necktitude Guideline
> Front-End Repository : https://github.com/vision-necktitude/front <br>
> Back-End Repository : https://github.com/vision-necktitude/server <br>
> AI Repository : https://github.com/vision-necktitude/computer-vision <br>

## Vision Necktitude
- 프로젝트명 : Vision Necktitude
- 프로젝트 목적 : 현대인의 컴퓨터 사용 습관 개선
- 개발 기간 : 23.03 ~ 24.06
<br><br>

### 팀원
| PM | Front-End | Back-End | AI |
|:--:|:--:|:--:|:--:|
| 조승민 |  정조은  | 강동석 | 이현석 |
<br>

### 서비스 소개
컴퓨터를 많이 사용하는 현대인들이 많이 겪는 고질병으로 안구건조증, 거북목 증후군이 있다. 이를 예방하고 악화를 막기 위해서는 올바른 컴퓨터 사용 습관을 가지는 것이 중요하다. Vision Necktitude는 안구건조증과 거북목 증후군을 예방할 수 있도록 사용자의 사용 습관 개선을 도와주는 서비스이다. 
<br><br>

### 주요 기능
1. 눈 깜빡임 감지 <br>
웹캠을 통해 눈 깜빡임 여부를 감지하고, 눈을 깜빡이는 간격을 확인한다.

2. 거북목 감지 <br>
웹캠을 통해 사용자가 거북목 상태를 유지하는지 확인한다. 거북목 상태 여부와 그 상태를 얼마나 유지했는지 확인한다.

3. 안구건조증, 거북목 증후군 정보 제공 <br>
안구건조증과 거북목 증후군의 정의, 예방 수칙 등을 확인할 수 있다.
<br><br>

### 기대 효과
1. 사용자들이 자연스럽게 컴퓨터 사용 습관을 개선한다.
2. 잘못된 자세로 인한 질병을 예방한다.
<br><br>

이 프로젝트는 OpenCV와 Mediapipe를 사용하여 카메라 기반의 눈 깜빡임 및 거북목 감지 시스템을 구현합니다. FastAPI 서버와 카메라 처리를 시작하고 중지하는 엔드포인트를 제공하며, 눈 깜빡임 및 거북목 자세를 감지하는 클래스가 포함되어 있습니다.

### 설치 사전 요구사항
Python 3.8 이상<br>
pip<br>

### 설치
```
pip install -r requirements.txt
```
OpenCV와 Mediapipe를 설치합니다
```
pip install opencv-python mediapipe
```
### 사용법<br>
서버 시작<br>

FastAPI 서버를 실행
```
uvicorn main:app --reload
```
서버가 http://127.0.0.1:8000에서 시작됩니다. Postman이나 cURL 같은 도구를 사용하여 엔드포인트를 테스트할 수 있습니다.

### 카메라 처리 시작 및 중지
카메라 처리를 시작하려면 /camera로 POST 요청을 보냅니다:
```
curl -X POST http://127.0.0.1:8000/camera
```

카메라 처리를 중지하려면 /camera/end로 POST 요청을 보냅니다:
```
curl -X POST http://127.0.0.1:8000/camera/end
```

프로젝트 구조<br>
camera-processing/<br>
│<br>
├── main.py                     # FastAPI 애플리케이션의 진입점<br> 
├── camera_component.py        # 카메라 처리 로직을 포함<br>
├── eye_blink_detector.py       # EyeBlinkDetector 클래스를 포함<br>
├── tech_neck_detector.py      # TechNeckDetector 클래스를 포함<br>
├── component/<br>
│   └── server_communicator.py  # ServerCommunicator 클래스를 포함<br>
├── requirements.txt           # 프로젝트 종속성 목록<br>
└── README.md                   # 프로젝트 README 파일<br>

## 엔드포인트
POST /camera<br>
카메라 처리를 시작합니다.

응답:

```json
{
    "message": "Camera processing started."
}
```

POST /camera/end<br>
카메라 처리를 중지합니다.

응답:

```json
{
    "message": "Camera is stopped."
}
```

### 컴포넌트
main.py<br>
카메라 처리를 시작하고 중지하는 엔드포인트를 가진 FastAPI 서버를 설정합니다.<br>
camera_component.py<br>
카메라에서 영상을 캡처하고 눈 깜빡임 및 거북목 감지를 실행하는 주요 로직을 포함합니다.<br>
eye_blink_detector.py<br>
Mediapipe를 사용하여 눈 깜빡임을 감지하고 눈 깜빡임 비율(EAR)을 계산하는 EyeBlinkDetector 클래스를 포함합니다.<br>
tech_neck_detector.py<br>
얼굴 및 신체 랜드마크를 기반으로 거북목 자세를 감지하는 TechNeckDetector 클래스를 포함합니다.<br>
component/server_communicator.py<br>
서버 통신을 처리하는 ServerCommunicator 클래스를 포함합니다 (세부 사항 제공되지 않음).<br>

### 이 프로젝트는 다음 라이브러리를 사용합니다
- OpenCV
- Mediapipe <br>

문제나 기여 사항이 있으면 GitHub 저장소에 티켓을 열어주세요.

