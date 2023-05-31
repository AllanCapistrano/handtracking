from typing import List

from numpy import bincount, argmax

def statistical_mode(numbers: List[int]) -> int:
    """ Retorna a moda estatística de um conjunto de números inteiros.

    Parameters
    ----------
    numbers: :class:`List[int]`
        Lista de números inteiros que se deseja encontrar a moda.

    Returns
    -------
    :class:`int`
    """

    return argmax(bincount(numbers))