import unittest

import numpy as np

from src.QDSim.QDSimulator import QDSimulator
from src.utilities.sampling import random_sampling, batch_random_sampling

class SamplingTest(unittest.TestCase):

    def test_sample(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        # read a tensor from a file
        sim = QDSimulator(path)
        # sample an element from the tensor
        i, s = random_sampling(sim)
        # check that the sampled element is in the tensor
        self.assertEqual(sim.sample(i), s)
        print('CSD[', i, '] = ', s)

    def test_sample_batch(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        # sample a batch of elements from the tensor
        batch_size = 10
        # read a tensor from a file
        sim = QDSimulator(path)
        # sample a batch of elements from the tensor
        batch = batch_random_sampling(sim, batch_size)
        # check that the sampled elements are in the tensor
        for i in batch.keys():
            self.assertEqual(sim.sample(i), batch[i])
            print('CSD[', i, '] = ', batch[i])


if __name__ == '__main__':
    unittest.main()
