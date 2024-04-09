

import cv2
from i eye_blink_detector
import tech_neck_detector


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
