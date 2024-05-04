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

    This is done with complexity ?????? and can be parallelized.
    - The batch size is estimated with complexity O(1).
    - Complexity of the sampling process is = O(1 / log(1 - d / l) where d is the number of dimensions and l is the tile density factor
    - The compression process is O(volume_(transition line)) = O(d * s ^ (d-1))
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
        the batch size must guarantee with an high confidence level that at least a transition line point is sampled.

        To to this, we estimate the probability of sampling a transition line point and use it to calculate the confidence of a binomial distribution.
        The result is ?????

        ----------------
        Proof
        ----------------
        Given that:
        - sensitivity s is the sensitivity of a single dimension of the simulated space
        - dimensions d is the number of dimensions of the simulated space
        - edge l is a parameter indicating the density of the transition lines

        Lets assume that hexagons are cubes XD... to simplify the problem we consider the space to be tiled with cubes
        instead of hexagons. This simplification is valid because the growth factor of the transition lines volume wrt d is the same.
        Under our cube simplification, the edge l is the edge of the cubes.

        Probability p is the probability of sampling a transition line point.
        p = volume_(transition line) / volume_(tot)

        The total volume formula is straightforward:
        volume_(tot) = s^d

        The transition line volume formula is more complex.
        We first count the transition line for each dimension. The transition line is an hyperplane of dimension d-1.
        N = s / l

        The transition line volume is the volume of an hyperplane of dimension d-1.
        volume_(row) = s ^ (d-1)

        Hence, the total transition line volume is the volume of a single hyperplane multiplied by the number of hyperplanes N * d,
        minus the volume of the intersections. The term of the intersections is the volume of an hyperplane of dimension d-2.
        However, we ignore the intersections because they don't affect the order of magnitude of the volume.
        volume_(transition line) = N * d * volume_(row) - intersections = N * d * s ^ (d-1)

        Finally, the probability of sampling a transition line point at random out of the total space, is
        p = N * d * s ^ (d-1) / s^d = s / l * d / s = d / l
        We notice that the probability scales linearly with the number of dimensions and the number of transition lines.
        Yay!

        We wish to have high confidence in sampling at least one transition line point.
        The probability of not sampling transition line point after b attempts is (1-p)^b.
        The probability of sampling at least one transition line point after b attempts is 1 - (1-p)^b.
        We want to compute b such that 1 - (1-p)^b >= c, where c is the confidence level.
        We can rewrite the inequality as (1-p)^b <= 1 - c and solve as follows if 1-p > 0:
        We can rewrite the inequality as b >= log(1 - c) / log(1 - p).
        and finally find b >= log(1 - c) / log(1 - d / l).
        
        The complexity of the sampling process is O(b(d)) where b is the batch size:
        O(1 / log(1 - d / l)
        This can be parallelized because the sampling process of a point is independent of the other points.
        
        # TODO BUG !!!!!
        This is wrong for two reasons:
        First, I don't expect the result to be a function of just d and l, without s. I would rather expect d and a tile density factor l/s.
        Second, if I plot the solution (see screenshot) I see that the solution does not grows with d, on the contrary it decreases exponentially, which is wrong.

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

    def random_sampling(self, batch_size: int) -> queue.Queue():
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

    def flood(self, to_process: queue.Queue):
        """
        This method fills the compressed binary CSD (bCSD) by starting with some transition line points,
        and then adding their transition line neighbors, and so on, like a flood that propagates in the water channels of the transition lines.
        The compressed binary CSD (bCSD) is a list of coordinates of transition line points.
        The CPU and memory complexity to compute the bCSD is the total volume of the transition lines, so is the size.
        The complexity of the flood process is O(volume_(transition line)) = O(d * s ^ (d-1)).
        The flood process can be parallelized because the computation of a point is independent of the other points.

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
        self.flood(to_process)
        return self.bCSD
