from numpy import array, uint8, ndarray
from cv2 import cvtColor, inRange, bitwise_and, COLOR_BGR2YCR_CB

def detect_skin(image: ndarray) -> ndarray:
    """ Retorna uma imagem contendo somente as regiões da pele.

    Parameters
    ----------
    image: :class:`ndarray`
        Imagem que se deseja fazer a detecção.

    Returns
    -------
    :class:`ndarray`
    """

    min_range = array([0,133,77], uint8)
    max_range = array([235,173,127], uint8)

    image_in_ycr = cvtColor(image, COLOR_BGR2YCR_CB)
    skin_area = inRange(image_in_ycr, min_range, max_range)
    detected_skin = bitwise_and(image, image, mask=skin_area)

    return detected_skin