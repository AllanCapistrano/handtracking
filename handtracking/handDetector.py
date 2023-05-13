from typing import List, Dict

from mediapipe import solutions
from cv2 import Mat, cvtColor, COLOR_BGR2RGB
from numpy import ndarray

THUMB_TIP: int = 4
INDEX_FINGER_TIP: int = 8
MIDDLE_FINGER_TIP: int = 12
RING_FINGER_TIP: int = 16
PINKY_TIP: int = 20

class HandDetector:
    def __init__(
        self, 
        image_mode: bool = False, 
        max_num_hands: int = 2,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5, 
        min_tracking_confidence: float = 0.5
    ) -> None:
        """ Método construtor.

        Parameters
        ----------
        image_mode: :class:`bool`
            Se deve tratar as imagens de entrada como um conjunto de imagens 
            estáticas ou um fluxo de vídeo.
        max_num_hands: :class:`int`
            Número máximo de mãos que presentes na imagem.
        model_complexity: :class:`int`
            Complexidade do modelo 'landmark' (0 ou 1).
        min_detection_confidence: :class:`float`
            Valor mínimo de confiança para que a detecção das mãos seja 
            considerada bem-sucedida.
        min_tracking_confidence: :class:`float`
            Valor mínimo de confiança para os pontos de referência das mãos 
            serem considerados rastreados com sucesso.
        """
        
        self.mediapipe_hands = solutions.hands
        self.hands = self.mediapipe_hands.Hands(
            image_mode,
            max_num_hands,
            model_complexity,
            min_detection_confidence,
            min_tracking_confidence
        )
        self.mediapipe_draw = solutions.drawing_utils

    def process_image(self, image: ndarray) -> None:
        """ Realiza o processamento de uma imagem, em BGR, para as próximas 
        operações.

        Parameters
        ----------
        image: :class:`ndarray`
            Imagem em BGR que será processada.
        """
        
        self.image = image

        image_rgb: Mat = cvtColor(image, COLOR_BGR2RGB)
        image_processed = self.hands.process(image_rgb)
        self.hands_landmarks = image_processed.multi_hand_landmarks
    
    def draw_landmarks(self, image: ndarray) -> ndarray:   
        """ Desenhas as marcações nas mãos presentes em uma imagem.

        Parameters
        ----------
        image: :class:`ndarray`
            Imagem em que será desenhada as marcações .
        
        Returns
        -------
        :class:`ndarray`
        """
        
        if(self.hands_landmarks):
            for hand_landmarks in self.hands_landmarks:
                self.mediapipe_draw.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mediapipe_hands.HAND_CONNECTIONS
                )

        return image
    
    def find_positions(self) -> List[Dict]:
        """ Retorna uma lista contendo as posições (eixo x e y, em pixels) dos 
        pontos de detecção das mãos presentes em uma imagem.

        Modelo: [{hand_id, landmarks: [{landmark_id, x, y}]}]
        
        Returns
        -------
        :class:`List[Dict]`
        """
        
        hands: list = []
        
        if(self.hands_landmarks):
            hand_id: int = 0
            
            for hand_landmarks in self.hands_landmarks:
                landmark_list: list = []
                hands.append({"hand_id": hand_id})

                for point_id, landmark_coordinates in enumerate(hand_landmarks.landmark):
                    img_height, img_width, _ = self.image.shape

                    # Convertendo as coordenadas de float para pixels.
                    landmark_x = int(landmark_coordinates.x * img_width)
                    landmark_y = int(landmark_coordinates.y * img_height)

                    landmark_list.append({
                        "landmark_id": point_id, 
                        "x": landmark_x, 
                        "y": landmark_y
                    })

                    hands[hand_id].update({"landmarks": landmark_list})

                hand_id += 1

        return hands
    
    def hand_orientation(self, hand: Dict) -> str:
        """ Indica se é a mão direita ou a mão esquerda, com base na posição do
        dedão e o dedo mindinho.

        Parameters
        ----------
        hand: :class:`List[Dict]`
            Dicionário contendo informações da mão. Ex: 
            {hand_id, landmarks: [{landmark_id, x, y}]}

        Returns
        -------
        :class:`str`
        """
        
        keys: List = hand.keys()
        keys_count: int = 0
        
        for key in keys:
            if(key == "hand_id"):
                keys_count += 1
            elif(key == "landmarks"):
                keys_count += 1

        if(keys_count == 2):
            if(hand["landmarks"][PINKY_TIP]["x"] >  hand["landmarks"][THUMB_TIP]["x"]):
                return "left"
            else:
                return "right"
            
    def number_fingers(self) -> int:
        """ Retorna o número de dedos que estão levantados.

        Returns
        -------
        :class:`int`
        """

        hands: List = self.find_positions()

        count_fingers: int = 0

        if(len(hands) > 0):
            for hand in hands:
                for index in range(len(hand["landmarks"])):
                    if(index == INDEX_FINGER_TIP):
                        finger_tip: int = hand["landmarks"][index]["y"]
                        finger_pip: int = hand["landmarks"][index - 2]["y"]
                        
                        if(finger_tip < finger_pip):
                            count_fingers += 1
                    elif(index == MIDDLE_FINGER_TIP):
                        finger_tip: int = hand["landmarks"][index]["y"]
                        finger_pip: int = hand["landmarks"][index - 2]["y"]
                        
                        if(finger_tip < finger_pip):
                            count_fingers += 1
                    elif(index == RING_FINGER_TIP):
                        finger_tip: int = hand["landmarks"][index]["y"]
                        finger_pip: int = hand["landmarks"][index - 2]["y"]
                        
                        if(finger_tip < finger_pip):
                            count_fingers += 1
                    elif(index == PINKY_TIP):
                        finger_tip: int = hand["landmarks"][index]["y"]
                        finger_pip: int = hand["landmarks"][index - 2]["y"]
                        
                        if(finger_tip < finger_pip):
                            count_fingers += 1
                    elif(index == THUMB_TIP):
                        thumb_tip: int = hand["landmarks"][THUMB_TIP]["x"]
                        index_finger_mcp: int = hand["landmarks"][5]["x"]
                        
                        if(abs(thumb_tip - index_finger_mcp) > 30):
                            count_fingers += 1
           
        return count_fingers