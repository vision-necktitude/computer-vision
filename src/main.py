# !/usr/local/bin/python3
# -*- coding:utf-8 -*-

import math
import time

import mediapipe as mp
import cv2
from scipy.spatial import distance

# import ray

CHIN = 152

# 광대 인덱스
LEFT_CHEEK = 234
RIGHT_CHEEK = 454

# 어깨 관련 특징점 인덱스
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12


# @ray.remote
class EyeBlinkDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.blink_count = 0
        self.pre_blink_state = False
        self.eyeCloseChecker = EyeCloseChecker()

    def calculate_EAR(self, eye):
        a = distance.euclidean((eye[0], eye[1]), (eye[2], eye[3]))
        # b = distance.euclidean((eye[0], eye[1]), (eye[2], eye[3]))
        c = distance.euclidean((eye[4], eye[5]), (eye[6], eye[7]))
        ear_aspect_ratio = a / c
        return ear_aspect_ratio

    # def get_eye_region(self, image, landmarks, left_indices, right_indices):
    #     eye_points = [(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])) for landmark in landmarks]
    #     eye_array = [eye_points[i] for i in left_indices] + [eye_points[i] for i in right_indices]
    #     return eye_array

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
        timer = self.eyeCloseChecker

        if ear is not None:
            # EAR 값이 0.36 이하인 경우
            if ear < 0.36:
                # 현재 눈 감음 상태가 아닌 경우
                if not self.pre_blink_state:
                    self.pre_blink_state = True
                    self.blink_count += 1
                    timer.startClose()
            else:
                self.pre_blink_state = False
                print(timer.endClose())

        cv2.putText(frame, f"Blink Count: {self.blink_count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame


# @ray.remote
class TechNeckDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.has_run = False
        self.initial_cheek_distance = 0
        self.initial_chin_shoulder_distance = 0
        self.tech_neck_threshold = 0

    def setInitialLength(self, cheek, chin_shoulder):
        time.sleep(3)
        self.initial_cheek_distance = cheek
        self.initial_chin_shoulder_distance = chin_shoulder
        self.tech_neck_threshold = self.initial_cheek_distance / self.initial_chin_shoulder_distance

    def detect_tech_neck(self, frame):
        image_height, image_width, _ = frame.shape
        results = self.holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.face_landmarks is not None and results.pose_landmarks is not None:
            left_cheek_coords = results.face_landmarks.landmark[LEFT_CHEEK]
            right_cheek_coords = results.face_landmarks.landmark[RIGHT_CHEEK]
            x_left_cheek = int(left_cheek_coords.x * image_width)
            y_left_cheek = int(left_cheek_coords.y * image_height)
            x_right_cheek = int(right_cheek_coords.x * image_width)
            y_right_cheek = int(right_cheek_coords.y * image_height)
            cheek_distance = math.dist((x_left_cheek, y_left_cheek), (x_right_cheek, y_right_cheek))

            chin_coords = results.face_landmarks.landmark[CHIN]
            left_shoulder_coords = results.pose_landmarks.landmark[LEFT_SHOULDER]
            right_shoulder_coords = results.pose_landmarks.landmark[RIGHT_SHOULDER]
            x_chin = int(chin_coords.x * image_width)
            y_chin = int(chin_coords.y * image_height)
            x_left_shoulder = int(left_shoulder_coords.x * image_width)
            y_left_shoulder = int(left_shoulder_coords.y * image_height)
            x_right_shoulder = int(right_shoulder_coords.x * image_width)
            y_right_shoulder = int(right_shoulder_coords.y * image_height)
            chin_shoulder_distance = abs(y_chin - ((y_left_shoulder + y_right_shoulder) // 2))

            return cheek_distance, chin_shoulder_distance
        else:
            return None

    def detect_and_draw_tech_neck(self, frame):
        results = self.detect_tech_neck(frame)
        if results is not None:
            cheek_distance, chin_shoulder_distance = results
            cv2.putText(frame, f"Cheek Distance: {cheek_distance}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2)
            cv2.putText(frame, f"Chin-Shoulder Distance: {chin_shoulder_distance}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
            if not self.has_run:
                self.setInitialLength(cheek_distance, chin_shoulder_distance)
                self.has_run = True
            # print("initial: {}, {}".format(self.initial_cheek_distance, self.initial_chin_shoulder_distance))

        return frame


class EyeCloseChecker:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0

    def startClose(self):
        self.startTime = time.time()

    def endClose(self):
        self.endTime = time.time()
        return round(self.startTime - self.endTime)


def main():
    # ray.init()

    # 카메라 셋팅
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    eye_blink_detector = EyeBlinkDetector()
    tech_neck_detector = TechNeckDetector()

    while True:
        _, frame = cap.read()

        # 눈깜빡임 감지와 카운트 수행
        frame = eye_blink_detector.detect_and_count_blinks(frame)
        # frame = ray.get(eye_blink_detector.detect_and_count_blinks.remote(frame))

        # 거북목 감지 수행
        frame = tech_neck_detector.detect_and_draw_tech_neck(frame)
        # frame = ray.get(tech_neck_detector.detect_and_draw_tech_neck.remote(frame))

        cv2.imshow("Combined Model", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    # ray.shutdown()


if __name__ == '__main__':
    main()
