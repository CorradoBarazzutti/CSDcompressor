from src.compressor import Compressor

def run_test1():
    path = '/Users/corrado/Desktop/CSDcompressor/src/QDSim/library/test1.txt'
    compressor = Compressor(path)
    compressor.run()

if __name__ == '__main__':
    run_test1()
