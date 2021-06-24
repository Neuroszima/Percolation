from time import time


def time_it(function):
    """
    measures time that takes for a function to execute
    :param function:
    :return:
    """
    def wrapper(*args, **kwargs):
        start = time()
        result = function(*args, **kwargs)
        end = time()
        diff = end - start
        print(f"{function.__name__} took {diff * 1000} milliseconds")
        return result

    return wrapper


def print_lat_3d(lat):
    print("3d lattice")
    for surface in lat:
        for line in surface:
            print(line)
        print()


def flatten_once(arr: list):
    tmp = []
    for i in arr:
        tmp.extend(i)
    return tmp


def find_shape(arr: list):
    """
    this function is designed to only work with arrays that has well defined shape/dimensions
    won't work on arrays with variable subarray lengths

    :param arr: array of unknown shape
    :return: nr. of dimensions, array shape, flattened array
    """
    tmp = arr[0]
    shape = [len(arr)]
    dimensions = 1
    while isinstance(tmp, (list, tuple)):
        shape.append(len(tmp))
        arr = flatten_once(arr)
        tmp = arr[0]
        dimensions += 1
        if dimensions > 6:  # for percolation purposes we will use up to 3 or 4 dimensions; while (True) prevention
            raise ValueError("too many dimensions")
    return dimensions, shape[::-1], arr


if __name__ == '__main__':
    from copy import deepcopy
    from random import random, seed

    seed(200)
    shape = [4, 5, 2, 4]
    p = 0.3
    a = [[[[1, 2], [3, 4], [5, 6]],
          [[7, 8], [9, 10], [11, 12]]],
         [[[1, 2], [3, 4], [5, 6]],
          [[7, 8], [9, 10], [11, 12]]]]
    lat = [[[[ 2 if random() < p else 1 for _ in range(shape[0])
              ] for __ in range(shape[1])
             ] for ___ in range(shape[2])
            ] for ____ in range(shape[3])]
    arr1 = deepcopy(a)
    arr2 = deepcopy(a)

    # flatten fully, well defined arrays will flatten in order, meanwhile arrays with varying nesting level will not
    a2 = [_ for _ in [arr1.extend(i) if isinstance(i, (list, tuple)) else i for i in arr1] if _]
    # with the use of function
    a3 = flatten_once(a)
    # a "flatten once" on well defined array will result the same results as below, otherwise the list comp will spit
    # out random order and information
    a_info = find_shape(lat)
    print(f"information: {a_info}")
    assert shape == a_info[1]
