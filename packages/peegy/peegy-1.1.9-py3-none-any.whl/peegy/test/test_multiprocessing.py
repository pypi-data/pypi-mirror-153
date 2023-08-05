__author__ = 'jundurraga-ucl'
import multiprocessing as mp
import numpy as np
# Define an output queue
output = mp.Queue()

# define a example function


def rand_string(x):
    """ Generates a random string of numbers, lower- and uppercase chars. """
    rand_str = np.random.random((1, 10000))
    print(rand_str)
    print('done:', x)


# Setup a list of processes that we want to run
processes = [mp.Process(target=rand_string, args=x) for x in range(4)]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
# for p in processes:
#     p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

print(results)
