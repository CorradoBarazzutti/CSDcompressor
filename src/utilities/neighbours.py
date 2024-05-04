import itertools


def d_infinity_neighbors(point: tuple, shape: list, distance: int = 1) -> list:
    """
    This method generates the coordinates of the d-infinity neighbors of a given point in a n-dimensional space.
    The d-infinity neighbors are the points that are at a distance of d from the given point by the d-infinity norm:
    ||x - y|| = max(|x_i - y_i|).

    To achieve this, the method uses itertools.product Cartesian product of your current location with each coordinate
    perturbed by d in each direction.

    E.g. d = 1. You'll have a list of triples derived from your current point as such: diag_coord = [(x-1, x, x+1) for x in point]
    Now, you take the product of all those triples, recombine each set, and you have your diagonals.

    :param point: tuple representing the point
    :param shape: list representing the dimensions of the space
    :param distance: the distance from the point

    :return: list of tuples representing the coordinates of the d-infinity neighbors points of the given point
    """
    if distance < 0:
        raise ValueError('Distance must be a positive integer')
    # TODO: implement for d > 1
    if distance != 1:
        raise ValueError('Not implemented yet')

    # compute the number of dimensions
    dimension = len(shape)

    # init neighbors list
    neighbors = []

    # generate the neighbors
    for delta in itertools.product([-1, 0, 1], repeat=dimension):
        # if the delta is the null vector, skip it
        if all([x == 0 for x in delta]):
            continue
        # get the coordinates of the neighbor
        neighbor = tuple([point[i] + delta[i] for i in range(dimension)])
        # check if the neighbor is in the simulator space
        if all(0 <= neighbor[i] < shape[i] for i in range(dimension)):
            neighbors.append(neighbor)

    return neighbors
