import mediapipe as mp
import cv2

import math
import time


# 턱 인덱스
CHIN = 152

# 광대 인덱스
LEFT_CHEEK = 234
RIGHT_CHEEK = 454

# 어깨 관련 특징점 인덱스
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

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

            distance_ratio = cheek_distance / chin_shoulder_distance
            if self.tech_neck_threshold is not None and distance_ratio > self.tech_neck_threshold * 1.2:
                print("TECH NECK!!!")
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