import cv2
import threading

from .eye_blink_detector import EyeBlinkDetector
from .tech_neck_detector import TechNeckDetector

TIMER_INTERVAL = 30

def main():
    global is_running
    is_running = True

    # 카메라 셋팅
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    eye_blink_detector = EyeBlinkDetector()
    tech_neck_detector = TechNeckDetector()

    tech_neck_detector.detectTechNeckForDuration()
    eye_blink_detector.detectEyeCloseForDuration()

    while is_running:
        _, frame = cap.read()

        # 눈깜빡임 감지와 카운트 수행
        frame = eye_blink_detector.detect_and_count_blinks(frame)

        # 거북목 감지 수행
        frame = tech_neck_detector.detect_and_draw_tech_neck(frame)

        cv2.imshow("Combined Model", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            is_running = False
        # tech_neck_detector.detectTechNeckForDuration()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
