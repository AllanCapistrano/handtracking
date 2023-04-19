from time import time

import cv2
from handDetector import HandDetector

WEBCAM_INDEX = 0

def main():
    fps_start_time = 0

    hand_detector = HandDetector()

    webcam = cv2.VideoCapture(WEBCAM_INDEX)

    while(True):
        success, frame = webcam.read()

        if(success):
            hand_detector.process_image(frame)
            image_with_landmarks = hand_detector.draw_landmarks()
            hands = hand_detector.find_positions()

            if(len(hands) > 0):
                print(hands[0]["landmarks"][6])

            fps_end_time = time()
            fps = 1/(fps_end_time - fps_start_time)
            fps_start_time = fps_end_time

            cv2.putText(image_with_landmarks, f"FPS: {int(fps)}", (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)

            cv2.imshow("Webcam", image_with_landmarks)
            key = cv2.waitKey(1)

            if(key == 81 or key == 113):
                break
    
    webcam.release()

if __name__ == "__main__":
    main()