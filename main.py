from time import time

import cv2
import mediapipe as mp

WEBCAM_INDEX = 0

webcam = cv2.VideoCapture(WEBCAM_INDEX)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

previous_time = 0
current_time = 0

while(True):
    success, img = webcam.read()

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    hands_landmarks = results.multi_hand_landmarks

    # TODO: Diferenciar as mãos

    if(hands_landmarks):
        for hand_landmarks in hands_landmarks:
            for point_id, landmark_coordinates in enumerate(hand_landmarks.landmark):
                img_height, img_width, _ = img.shape

                # Convertendo coordenadas para pixels.
                landmark_x = int(landmark_coordinates.x * img_width)
                landmark_y = int(landmark_coordinates.y * img_height)

                print(point_id, landmark_x, landmark_y)


            mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)


    current_time = time()
    
    fps = 1/(current_time - previous_time)
    
    previous_time = current_time

    cv2.putText(img, f"FPS: {int(fps)}", (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)

    cv2.imshow("Webcam", img)

    cv2.waitKey(1)