import numpy as np

from src.QDSim.QDSimulator import QDSimulator

def random_sampling(sim: QDSimulator) -> tuple:
    """
    Given an N-dimensional tensor of floats, sample a random float element from it.
    Return a tuple containing the indices of the sampled element and the element itself.

    Parameters:
    tensor (np.ndarray): a tensor of floats

    :return a tuple containing:
    a tuple of the indices of the sampled element
    the element itself
    """
    # sample an index for each dimension
    indices = tuple([np.random.randint(dim) for dim in sim.get_shape()])
    # return the element at the sampled indices
    return indices, sim.sample(indices)

def batch_random_sampling(sim: QDSimulator, batch_size: int) -> list:
    """
    Given an N-dimensional tensor of floats, sample a batch of random float element from it.
    Return a dict containing the indices of the sampled element and the element itself.

    Parameters:
    tensor (np.ndarray): a tensor of floats
    batch_size (int): the number of elements to sample

    :return a dict such that each key, value pair contains:
    a tuple of the indices of the sampled element as the key
    the element itself as the value
    """
    # TODO parallelize this
    return dict(random_sampling(sim) for _ in range(batch_size))
