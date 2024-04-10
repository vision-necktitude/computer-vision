import mediapipe as mp
import cv2

import time
import threading
from scipy.spatial import distance

pastEyeBlinkCount = 0

class EyeBlinkDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.blinkCount = 0
        self.pre_blink_state = False
        self.eyeBlinkChecker = EyeBlinkChecker()
        self.timerInterval = 60

    def calculate_EAR(self, eye):
        a = distance.euclidean((eye[0], eye[1]), (eye[2], eye[3]))
        # b = distance.euclidean((eye[0], eye[1]), (eye[2], eye[3]))
        c = distance.euclidean((eye[4], eye[5]), (eye[6], eye[7]))
        ear_aspect_ratio = a / c
        return ear_aspect_ratio

    def detect_eye_blink(self, frame):
        image_height, image_width, _ = frame.shape
        left_eye = self.getLeftEye(frame)
        right_eye = self.getRightEye(frame)

        # 좌표를 이용하여 원을 그립니다.
        if left_eye is not None and right_eye is not None:
            cv2.circle(frame, (int(left_eye[0]), int(left_eye[1])), 3, (0, 0, 255), 1)
            cv2.circle(frame, (int(left_eye[2]), int(left_eye[3])), 3, (0, 0, 255), 1)
            cv2.circle(frame, (int(left_eye[4]), int(left_eye[5])), 3, (0, 0, 255), 1)
            cv2.circle(frame, (int(left_eye[6]), int(left_eye[7])), 3, (0, 0, 255), 1)

            cv2.circle(frame, (int(right_eye[0]), int(right_eye[1])), 3, (0, 0, 255), 1)
            cv2.circle(frame, (int(right_eye[2]), int(right_eye[3])), 3, (0, 0, 255), 1)
            cv2.circle(frame, (int(right_eye[4]), int(right_eye[5])), 3, (0, 0, 255), 1)
            cv2.circle(frame, (int(right_eye[6]), int(right_eye[7])), 3, (0, 0, 255), 1)

            left_ear = self.calculate_EAR(left_eye)
            right_ear = self.calculate_EAR(right_eye)
            ear = (left_ear + right_ear) / 2
            ear = round(ear, 2)
            print(ear)
            return ear

    def getLeftEye(self, image):
        results = self.holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.face_landmarks is not None:
            # landmarks = results.face_landmarks.landmark
            eye_top_x = int(results.face_landmarks.landmark[159].x * image.shape[1])
            eye_top_y = int(results.face_landmarks.landmark[159].y * image.shape[0])
            eye_left_x = int(results.face_landmarks.landmark[33].x * image.shape[1])
            eye_left_y = int(results.face_landmarks.landmark[33].y * image.shape[0])
            eye_bottom_x = int(results.face_landmarks.landmark[145].x * image.shape[1])
            eye_bottom_y = int(results.face_landmarks.landmark[145].y * image.shape[0])
            eye_right_x = int(results.face_landmarks.landmark[133].x * image.shape[1])
            eye_right_y = int(results.face_landmarks.landmark[133].y * image.shape[0])
            left_eye = (
            eye_top_x, eye_top_y, eye_bottom_x, eye_bottom_y, eye_left_x, eye_left_y, eye_right_x, eye_right_y)
            return left_eye

    def getRightEye(self, image):
        results = self.holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.face_landmarks is not None:
            eye_top_x = int(results.face_landmarks.landmark[386].x * image.shape[1])
            eye_top_y = int(results.face_landmarks.landmark[386].y * image.shape[0])
            eye_left_x = int(results.face_landmarks.landmark[362].x * image.shape[1])
            eye_left_y = int(results.face_landmarks.landmark[362].y * image.shape[0])
            eye_bottom_x = int(results.face_landmarks.landmark[374].x * image.shape[1])
            eye_bottom_y = int(results.face_landmarks.landmark[374].y * image.shape[0])
            eye_right_x = int(results.face_landmarks.landmark[263].x * image.shape[1])
            eye_right_y = int(results.face_landmarks.landmark[263].y * image.shape[0])
            right_eye = (
            eye_top_x, eye_top_y, eye_bottom_x, eye_bottom_y, eye_left_x, eye_left_y, eye_right_x, eye_right_y)
            return right_eye

    def close(self, frame):
        cv2.putText(frame, "CLOSED!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)

    def detect_and_count_blinks(self, frame):
        ear = self.detect_eye_blink(frame)
        timer = self.eyeBlinkChecker

        if ear is not None:
            # EAR 값이 0.36 이하인 경우
            if ear < 0.36:
                # 현재 눈 감음 상태가 아닌 경우
                if not self.pre_blink_state:
                    self.pre_blink_state = True
                    self.blinkCount += 1
                    timer.startClose()
            else:
                self.pre_blink_state = False
                timer.endClose()
                # print(f"blink time: {timer.endClose()}")

        cv2.putText(frame, f"Blink Count: {self.blinkCount}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame

    def detectEyeCloseForDuration(self):
        print(f"max eye blink: {self.eyeBlinkChecker.maxBlinkDuration}")
        self.eyeBlinkChecker.resetBlinkDurations()
        timer_thread = threading.Timer(self.timerInterval, self.detectEyeCloseForDuration)
        timer_thread.start()

        global pastEyeBlinkCount
        nowEyeBlinkCount = self.blinkCount
        count = nowEyeBlinkCount - pastEyeBlinkCount
        pastEyeBlinkCount = nowEyeBlinkCount
        print(f"eye blink count: {count}")

class EyeBlinkChecker:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.blinkDurations = []  # 눈 깜빡임 시간을 기록하는 리스트
        self.maxBlinkDuration = 0  # 최대 눈 깜빡임 시간

    def startClose(self):
        self.startTime = time.time()

    def endClose(self):
        self.endTime = time.time()
        blinkDuration = round(self.endTime - self.startTime, 2)
        self.blinkDurations.append(blinkDuration)  # 깜빡임 시간을 리스트에 추가
        self.maxBlinkDuration = max(self.maxBlinkDuration, blinkDuration)  # 최대 깜빡임 시간 갱신
        return blinkDuration

    def resetBlinkDurations(self):
        self.blinkDurations.clear()  # 깜빡임 시간 리스트 초기화
        self.maxBlinkDuration = 0  # 최대 깜빡임 시간 초기화