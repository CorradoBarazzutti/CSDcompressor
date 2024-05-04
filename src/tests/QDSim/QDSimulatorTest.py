import unittest
from src.QDSim.QDSimulator import QDSimulator

class QDSimulatorTest(unittest.TestCase):

    def test_init(self):
        sim = QDSimulator('/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt')
        print(sim)

    def test_sample(self):
        sim = QDSimulator('/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt')
        print(sim.sample((0, 0)))


if __name__ == '__main__':
    unittest.main()
