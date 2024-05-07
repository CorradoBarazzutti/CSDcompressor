import unittest

from src.flooder.flooder import Flooder


class FlooderTest(unittest.TestCase):

    def test_load(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        flooder = Flooder(path)

    def test_estimate_batch_size(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        flooder = Flooder(path)
        batch_size = flooder.estimate_batch_size()
        # assert batch_size is an integer and equal 5
        self.assertEqual(batch_size, 14)

    def test_sampling(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        flooder = Flooder(path)
        batch_size = flooder.estimate_batch_size()
        to_process = flooder.random_sampling(batch_size)
        # assert to_process is a queue and not empty
        self.assertTrue(to_process)

    def test_normalize(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        flooder = Flooder(path)
        batch_size = flooder.estimate_batch_size()
        to_process = flooder.random_sampling(batch_size)
        self.assertEqual(flooder.normalize(0.1), 0)
        self.assertEqual(flooder.normalize(0.9), 1)

    def test_get_neighbors(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        flooder = Flooder(path)
        batch_size = flooder.estimate_batch_size()
        to_process = flooder.random_sampling(batch_size)
        self.assertEqual(flooder.get_transition_line_neighbors((0, 0)), [(1, 1)])
        self.assertEqual(flooder.get_transition_line_neighbors((1, 1)), [(0, 0), (2, 2)])


    def test_compress(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        flooder = Flooder(path)
        batch_size = flooder.estimate_batch_size()
        to_process = flooder.random_sampling(batch_size)
        flooder.flood(to_process)
        # assert bCSD is not empty
        self.assertTrue(flooder.bCSD)

    def test_run(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        flooder = Flooder(path)
        flooder.run()
        # assert bCSD is not empty
        self.assertTrue(flooder.bCSD)


if __name__ == '__main__':
    unittest.main()
