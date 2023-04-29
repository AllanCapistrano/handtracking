from typing import List, Dict

from mediapipe import solutions
from cv2 import Mat, cvtColor, COLOR_BGR2RGB

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

    def process_image(self, image) -> None:
        """ Realiza o processamento de uma imagem, em BGR, para as próximas 
        operações.

        Parameters
        ----------
        image: :class:`bool`
            Imagem em BGR que será processada.
        """
        
        self.image = image

        image_rgb: Mat = cvtColor(image, COLOR_BGR2RGB)
        image_processed = self.hands.process(image_rgb)
        self.hands_landmarks = image_processed.multi_hand_landmarks
    
    def draw_landmarks(self) -> Mat:   
        """ Desenhas as marcações nas mãos presentes em uma imagem.
        
        Returns
        -------
        imagem: :class:`Mat`
        """
        
        if(self.hands_landmarks):
            for hand_landmarks in self.hands_landmarks:
                self.mediapipe_draw.draw_landmarks(
                    self.image, 
                    hand_landmarks,
                    self.mediapipe_hands.HAND_CONNECTIONS
                )

        return self.image
    
    
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
