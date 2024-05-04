import unittest

from src.compressor import Compressor


class CompressorTest(unittest.TestCase):

    def test_load(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        compressor = Compressor(path)

    def test_estimate_batch_size(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        compressor = Compressor(path)
        batch_size = compressor.estimate_batch_size()
        # assert batch_size is an integer and equal 5
        self.assertEqual(batch_size, 14)

    def test_sampling(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        compressor = Compressor(path)
        batch_size = compressor.estimate_batch_size()
        to_process = compressor.random_sampling(batch_size)
        # assert to_process is a queue and not empty
        self.assertTrue(to_process)

    def test_normalize(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        compressor = Compressor(path)
        batch_size = compressor.estimate_batch_size()
        to_process = compressor.random_sampling(batch_size)
        self.assertEqual(compressor.normalize(0.1), 0)
        self.assertEqual(compressor.normalize(0.9), 1)

    def test_get_neighbors(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        compressor = Compressor(path)
        batch_size = compressor.estimate_batch_size()
        to_process = compressor.random_sampling(batch_size)
        self.assertEqual(compressor.get_transition_line_neighbors((0, 0)), [(1, 1)])
        self.assertEqual(compressor.get_transition_line_neighbors((1, 1)), [(0, 0), (2, 2)])


    def test_compress(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        compressor = Compressor(path)
        batch_size = compressor.estimate_batch_size()
        to_process = compressor.random_sampling(batch_size)
        compressor.compression(to_process)
        # assert bCSD is not empty
        self.assertTrue(compressor.bCSD)

    def test_run(self):
        path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
        compressor = Compressor(path)
        compressor.run()
        # assert bCSD is not empty
        self.assertTrue(compressor.bCSD)


if __name__ == '__main__':
    unittest.main()
