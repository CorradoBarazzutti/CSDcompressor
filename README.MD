# CSDcompressor
This is a python package that finds a sparse and binary representation of a Charge Stability Diagrams (CSD), or bCSD of short.
This is achieved using by sampling the CSD and without any prior knowledge of the CSD.
The package is designed to work with the QDSim simulator: https://gitlab.com/QMAI/papers/qdsim/

## Procedure
1. Random sampling batch size estimation
2. Random sampling:
   1. Randomly sample points from the Charge Stability Diagram (CSD)
   2. Use the sampled points to establish the intensity range for the CSD. 
   3. Use the intensity range to rectify the CSD intensities. A binary step function (https://en.wikipedia.org/wiki/Heaviside_step_function) is applied to obtain the binary image (bCSD).
3. Compression: Flood fill the CSD, starting from the sampled points, to obtain the connected components.

## TODO s
### Clock
### Parallelize the code
```python
import threading
import queue

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

threading.Thread(target=worker, daemon=True).start()

for item in range(30):
    q.put(item)

q.join()
print('All work completed')
```