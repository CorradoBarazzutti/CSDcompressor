## Procedure
1. Randomly sample points from the Charge Stability Diagram (CSD)
2. Use the sampled points to establish the intensity range for the CSD. 
3. Use the intensity range to rectify the CSD intensities. A binary step function (https://en.wikipedia.org/wiki/Heaviside_step_function) is applied to obtain the binary image (bCSD).


## TODO 
### Clock
### Parallelize the code
import threading
import queue

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(30):
    q.put(item)

# Block until all tasks are done.
q.join()
print('All work completed')