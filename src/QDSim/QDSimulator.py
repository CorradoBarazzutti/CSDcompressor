from pathlib import Path
import numpy as np

from src.utilities.clock import Clock


class QDSimulator:

    def __init__(self, path: Path):
        # Load the np.tensor from the path
        self.__diagram = np.loadtxt(path)

    def get_shape(self):
        return self.__diagram.shape

    def __str__(self):
        return str(self.__diagram)

    def sample(self, indexes: tuple, clock: Clock = None) -> float:
        return self.__diagram[tuple(indexes)]
