import concurrent.futures
from random import random
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor

from pathfinding import find_path_2D, find_path_3D
from misc import time_it


def worker_2d(vals):
    """
    this function encapsulates generating lattices for 2d percolation problem and invoking pathfinding
    this is used for multiprocessing future obects in executor
    this can't be put in as local function since functions have to be pre-pickled into it

    :param vals: tuple wrapper for (propability, samples, lattice_size,)
    :return: number of times percolation did occur in lattice
    """
    v = vals[0]
    su_rate = 0
    for i in range(v[1]):
        lat = lattice_gen_2D(v[2], v[2], v[0])
        if find_path_2D([[True] + line + [True] for line in lat]):
            su_rate += 1
    return [v[2], v[0], su_rate]


def worker_3d(vals):
    """
    same as 2d version of this worker

    :param vals: tuple wrapper for (propability, samples, lattice_size,)
    :return: number of times percolation did occur in lattice
    """
    v = vals[0]
    su_rate = 0
    for i in range(v[1]):
        lat = lattice_gen_3D(v[2], v[2], v[2], v[0])
        if find_path_3D([[[True] + line + [True] for line in surface]
                         for surface in lat]):
            su_rate += 1
    return [v[2], v[0], su_rate]


def lattice_gen_2D(x=10, y=10, p=0.1):
    return [[True if random() < p else False for _ in range(x)]
            for _ in range(y)]


def lattice_gen_3D(x=6, y=6, z=6, p=0.1):
    return [[[True if random() < p else False for _ in range(x)]
             for _ in range(y)]
            for _ in range(z)]


class Percolation:
    def __init__(self, starting_size=4, end_size=10,
                 start_propablity=0.2, end_propability=0.6, step=0.05,
                 samples=70):
        self.s_s = starting_size
        self.e_s = end_size
        self.s_p = start_propablity
        self.e_p = end_propability
        self._step = step
        self._samples = samples
        self.__data = []

    def get_propablity_set(self):
        power = 0
        st = deepcopy(self._step)
        for _ in range(5):
            if st < 1:
                st *= 10
                power += 1
            else:
                break

        p_count = int(int(self.e_p * (10 ** power) - self.s_p * (10 ** power)) / int(st))
        return [self.s_p + self._step * p for p in range(p_count)]

    def get_results(self):
        return self.__data

    def start_sampling(self):
        pass

    def plot(self):
        pass


class Percolation2D(Percolation):
    def __init__(self, starting_size=4, end_size=13,
                 start_propablity=0.2, end_propability=0.65, step=0.03,
                 samples=100):
        super(Percolation2D, self).__init__(starting_size=starting_size,
                                            end_size=end_size,
                                            start_propablity=start_propablity,
                                            end_propability=end_propability,
                                            step=step, samples=samples)
        self.__data = []

    def start_sampling(self):
        sizes = list(range(self.s_s, self.e_s))
        for size in sizes:
            size_set = []
            # print("size " + str(size))
            for pr in self.get_propablity_set():
                success_rate = 0
                for i in range(self._samples):
                    lat = lattice_gen_2D(size, size, pr)
                    # horizontal test
                    if find_path_2D([[True] + line + [True] for line in lat]): success_rate += 1
                size_set.append([size, pr, success_rate])
            self.__data.append(size_set)

    def multiprocessed_sampling_2d(self):
        sizes = list(range(self.s_s, self.e_s))
        for size in sizes:
            size_set = []
            with ProcessPoolExecutor() as pex:
                props_ = [(pr, self._samples, size) for pr in self.get_propablity_set()]
                ppool = [pex.submit(worker_2d, (i,)) for i in props_]
                for f in concurrent.futures.as_completed(ppool):
                    size_set.append(f.result())

            self.__data.append(size_set)


class Percolation3D(Percolation):
    def __init__(self, starting_size=4, end_size=10,
                 start_propablity=0.2, end_propability=0.6, step=0.05,
                 samples=100):
        super(Percolation3D, self).__init__(starting_size=starting_size,
                                            end_size=end_size,
                                            start_propablity=start_propablity,
                                            end_propability=end_propability,
                                            step=step, samples=samples)
        self.__data = []

    def start_sampling(self):
        sizes = list(range(self.s_s, self.e_s))
        for size in sizes:
            size_set = []
            for pr in self.get_propablity_set():
                success_rate = 0
                for i in range(self._samples):
                    lat = lattice_gen_3D(size, size, size, pr)
                    # horizontal test
                    if find_path_3D([[[True] + line + [True]
                                      for line in surface]
                                     for surface in lat]):
                        success_rate += 1
                size_set.append([size, pr, success_rate])
            self.__data.append(size_set)

    def multiprocessed_sampling_3d(self):
        sizes = list(range(self.s_s, self.e_s))
        for size in sizes:
            size_set = []
            with ProcessPoolExecutor() as pex:
                props_ = [(pr, self._samples, size) for pr in self.get_propablity_set()]
                ppool = [pex.submit(worker_3d, (i,)) for i in props_]
                for f in concurrent.futures.as_completed(ppool):
                    size_set.append(f.result())

            self.__data.append(size_set)

if __name__ == '__main__':
    perc_2d = Percolation2D()
    time_it(perc_2d.start_sampling)()
    time_it(perc_2d.multiprocessed_sampling_2d)()
    perc_3d = Percolation3D()
    time_it(perc_3d.start_sampling)()
    time_it(perc_3d.multiprocessed_sampling_3d)()
