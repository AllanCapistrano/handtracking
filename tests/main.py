from time import time
from typing import List, Dict
from os import getenv

from dotenv import load_dotenv
import cv2

from handtracking import HandDetector

load_dotenv()

# ------------------------------- CONSTANTES ----------------------------------#
try:
    WEBCAM_INDEX = int(getenv("WEBCAM_INDEX"))
except:
    print("Erro! O valor de 'WEBCAM_INDEX' deve ser um número inteiro.")
    exit()
# -----------------------------------------------------------------------------#

def main():
    fps_start_time: float = 0

    hand_detector = HandDetector()

    webcam = cv2.VideoCapture(WEBCAM_INDEX)

    fps_flag: bool = True

    while(True):
        success, frame = webcam.read()

        if(success):
            key = cv2.waitKey(1)

            hand_detector.process_image(frame)
            image_with_landmarks = hand_detector.draw_landmarks(frame)
            hands: List[Dict] = hand_detector.find_positions()

            if(len(hands) > 0):
                print(hands[0]["landmarks"][6])

            fps_end_time: float = time()
            fps: float = 1/(fps_end_time - fps_start_time)
            fps_start_time: float = fps_end_time

            if(key == 81 or key == 113): # q ou Q
                break
            elif(key == 80 or key == 112): # p ou P
                fps_flag = not fps_flag

            if(fps_flag):
                cv2.putText(image_with_landmarks, f"FPS: {int(fps)}", (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)

            cv2.imshow("Webcam", image_with_landmarks)
        else:
            print("Não foi possível iniciar a webcam!")
            exit()
    
    webcam.release()

if __name__ == "__main__":
    main()