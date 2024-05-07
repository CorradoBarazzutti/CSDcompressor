# CSDcompressor
This is a python package that finds a compressed representation of a Charge Stability Diagram (CSD).
Multiple methods are available to compress the CSD, with attention to performance and parallelization.
The package is designed to work with the QDSim simulator: https://gitlab.com/QMAI/papers/qdsim/

## Methods available

### Sparse Binary Charge Stability Diagram (bCSD)
A sparse and binary representation of a Charge Stability Diagrams (CSD), or bCSD of short.
This is achieved using by sampling some points of the CSD and without any prior knowledge of the CSD.

#### Procedure
1. Random sampling batch size estimation
2. Random sampling:
   1. Randomly sample points from the Charge Stability Diagram (CSD)
   2. Use the sampled points to establish the intensity range for the CSD. 
   3. Use the intensity range to rectify the CSD intensities. A binary step function (https://en.wikipedia.org/wiki/Heaviside_step_function) is applied to obtain the binary image (bCSD).
3. Compression: Flood fill the CSD, starting from the sampled points, to obtain the connected components.

#### Issues
The Flood Fill algorithm and representation of the CSD scales with exp(d-1) where d is the number of dimensions of the CSD.

### Parametrized honeycomb
A parametrized grid representation of the Charge Stability Diagram (CSD).
This method is based on the assumption that the CSD has a geometric structure that can be represented by an honeycomb grid,
completely defined by a few parameters.
We wish to fit those parameters to samples from the bCSD to obtain a compressed representation of the CSD.

#### Honeycomb grid
The honeycomb grid in two dimensions is a grid of hexagons. 
Finding the honeycomb grid parameters seems like an hard geometric problem 
and also we don't now how to generalize it two higher dimensions (maybe the permuthaedron?)
so we start by simplifying the problem to a square grid.

Given that an object in an d-dimensional space has
- d degrees of freedom for translation
- d(d-1)/2 degrees of freedom for rotation

A square grid in d dimensions is defined by the following parameters:
- Edge scalar length L: L in R
- Intercept vector I: I in N+ ^ d
- Tilt vector Theta, representing the grid tilt on every degree of freedom: Theta in [0, 2pi) ^ d(d-1)/2
That is d+1+d(d-1)/2 parameters in total, or O(d^2)

#### Approachs
Multiple approaches are available to fit the honeycomb grid to the bCSD:
1. Grid regression: Fit the honeycomb grid parameters to the bCSD samples using a regression algorithm.
2. Grid clustering: Find the honeycomb grid parameters using a clustering algorithm on the bCSD samples.
3. NN encoding: encode the bCSD samples using a neural network to obtain the honeycomb grid parameters.

##### Grid regression
The grid regression is a regression problem where the input is a bCSD samples and the output is the honeycomb grid parameters.
Smart sampling should be used to avoid producing degenerate datapoints.
A norm should be used to measure the distance between the honeycomb grid and the bCSD samples.
The least square method can be used to find the honeycomb grid parameters but derivatives should probably be computed.

###### SOTA
This seems to be a known problem but only for square grids in two dimensions
* linear algebra approach https://stackoverflow.com/questions/62946604/fitting-an-orthogonal-grid-to-noisy-coordinates
* mathlab function ? https://www.mathworks.com/help/matlab/ref/griddata.html
* many approaches https://stackoverflow.com/questions/14219700/algorithm-for-fitting-points-to-a-grid?rq=4
* https://stackoverflow.com/questions/31426964/fitting-a-grid-to-data has no answer.

###### Norm
Our norm should define the distance between a point in the space and the closest point of the grid.
This defines the residual: a residual being the difference between a value sampled by the bCSD and the closest point in the grid.

###### Least Squares Method
The Least Squares Method consists in minimizing the sum of the squares of the residuals 
(a residual being the difference between an observed value and the fitted value provided by a model) 
made in the results of each individual equation.

To do this we need to compute the derivatives of the sum of squared residuals by the grid parameters.

## TODOs

### Clock
Implement a virtual timer to measure the time taken by the compression methods.

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

### Simulation from parameters

### Smart sampling
Random sampling is not efficient. We can use a smart sampling algorithm to sample the CSD.
