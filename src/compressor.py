import math
from pathlib import Path
import queue

import numpy as np

from src.QDSim.QDSimulator import QDSimulator
from src.utilities.sampling import batch_random_sampling
from src.utilities.neighbours import d_infinity_neighbors
from src.utilities.orderedSetQueue import OrderedSetQueue


class Compressor:
    """
    This class finds a compressed binary representation of a Charger Stability Diagram (CSD), or bCSD for short.
    This is achieved by sampling from a simulator without any prior knowledge of the CSD.
    This is done with complexity ?????? and is parallelizable.
    """

    def __init__(self, path: Path()):
        self.sim = QDSimulator(path)
        self.max_value = None
        self.min_value = None
        self.to_process = OrderedSetQueue()
        self.bCSD = []

    def estimate_batch_size(self) -> int:
        """
        This method estimates the batch size for the sampling process.
        the batch size must guarantee with an high confidence level that at least a transition line points are sampled.

        TODO confidence level formula
        TODO confirm the estimation formula
        TODO compute complexity of the sampling process

        :return: the estimated batch size
        """
        # get the dimensions of the simulator
        shape = self.sim.get_shape()
        # calculate the volume of the simulator
        volume = math.prod(shape)
        # calculate the batch size
        batch_size = int(volume * math.pow(0.1, len(shape) - 1)) + int(math.log(volume))
        print('sampling batch size is ', batch_size)
        return batch_size

    def random_sampling(self, batch_size: int = 1000) -> queue.Queue():
        """
        This method samples the simulator at random to get some transition line points.
        Sampled points are used to normalize the CSD values and initiate the compression process queue.

        TODO parallelize the sampling process

        :param batch_size: the size of the batch to sample
        :return: the process queue initialized with some transition line points
        """

        # sample the batch
        batch_sample = batch_random_sampling(self.sim, batch_size)

        # extract the max and min values of the batch sample dict values
        self.max_value = max(batch_sample.values())
        print('max value is ', self.max_value)
        self.min_value = min(batch_sample.values())
        print('min value is ', self.min_value)

        # rectify the batch sample
        rectified_batch_sample = dict()
        for key, value in batch_sample.items():
            rectified_batch_sample[key] = self.normalize(value)

        # extract the transition line points from the batch sample
        for key, value in rectified_batch_sample.items():
            if value == 1:
                self.to_process.put(key)

        return self.to_process

    def normalize(self, value: float) -> int:
        """
        This method normalizes the CSD values of the simulator

        :param value: the CSD value to normalize
        :return: the normalized value, either 0 or 1
        """
        if self.max_value is None or self.min_value is None:
            raise ValueError('Max and min values are not set. Please run the sample method first')

        average = (self.max_value + self.min_value) / 2
        if value < average:
            return 0
        else:
            return 1

    def get_transition_line_neighbors(self, point: tuple, distance: int = 1) -> list:
        """
        This method returns the neighbors of a given point if such neighbors are in the transition line.
        A d-infinity norm is used, see the d_infinity_neighbors method in the utilities module for more details.

        :param point: the coordinates of the target point
        :param distance: the distance from the point
        :return: the coordinates of the transition line neighbors of the given point
        """
        neighbors = []
        for neighbor in d_infinity_neighbors(point, self.sim.get_shape(), distance):
            if self.normalize(self.sim.sample(neighbor)) == 1:
                neighbors.append(neighbor)
        return neighbors

    def compression(self, to_process: queue.Queue):
        """
        This method fills the compressed binary CSD (bCSD) sampling .
        The compressed binary CSD (bCSD) is a list of coordinates of transition line points.
        # process each element of the transition line points list while adding new points to the list

        # TODO implement retries for d > 1

        :param to_process: the process queue initialized with some transition line points
        """
        # until the queue is empty
        while not to_process.empty():
            # get a point in the queue to be processed
            # TODO add mutex on the following two lines to prevent the race condition at:
            #  if neighbor not in self.bCSD: to_process.put(neighbor) ????
            #  or perhaps implement the following two lines in the OrderedSetQueue class
            point = to_process.get()
            self.bCSD.append(point)
            # get the neighbors of the point
            # TODO implement retries for d > 1
            neighbors = self.get_transition_line_neighbors(point)
            # for each transition line neighbor of the point
            for neighbor in neighbors:
                # if the neighbor has not been processed yet
                # TODO !!!! this invites race conditions: the neighbor could be added to the bCSD by another thread after the check
                # check https://stackoverflow.com/questions/16506429/check-if-element-is-already-in-a-queue
                if neighbor not in self.bCSD:
                    # add the neighbor to the queue
                    to_process.put(neighbor)

        print('bCSD is: ', self.bCSD)

    def run(self) -> list:
        """
        This method runs the compression process and returns the compressed binary CSD (bCSD).

        :return: the compressed binary CSD (bCSD)
        """
        batch_size = self.estimate_batch_size()
        to_process = self.random_sampling(batch_size)
        self.compression(to_process)
        return self.bCSD
