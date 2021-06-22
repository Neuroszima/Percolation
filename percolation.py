from random import random
from copy import deepcopy

from pathfinding import find_path_2D, find_path_3D


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


class Percolation_2D(Percolation):
    def __init__(self, starting_size=4, end_size=13,
                 start_propablity=0.2, end_propability=0.65, step=0.03,
                 samples=100):
        super(Percolation_2D, self).__init__(starting_size=starting_size,
                                             end_size=end_size,
                                             start_propablity=start_propablity,
                                             end_propability=end_propability,
                                             step=step, samples=samples)
        self.__data = []

    def start_sampling(self):
        sizes = list(range(self.s_s, self.e_s))
        for size in sizes:
            size_set = []
            print("size " + str(size))
            for pr in self.get_propablity_set():
                success_rate = 0
                for i in range(self._samples):
                    lat = lattice_gen_2D(size, size, pr)
                    # horizontal test
                    if find_path_2D([[True] + line + [True] for line in lat]): success_rate += 1
                size_set.append([size, pr, success_rate])
            self.__data.append(size_set)


class Percolation_3D(Percolation):
    def __init__(self, starting_size=4, end_size=10,
                 start_propablity=0.2, end_propability=0.6, step=0.05,
                 samples=100):
        super(Percolation_3D, self).__init__(starting_size=starting_size,
                                             end_size=end_size,
                                             start_propablity=start_propablity,
                                             end_propability=end_propability,
                                             step=step, samples=samples)
        self.__data = []

    def start_sampling(self):
        sizes = list(range(self.s_s, self.e_s))
        for size in sizes:
            print("size" + str(size))
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


if __name__ == '__main__':
    perc_2d = Percolation_2D()
    perc_2d.start_sampling()
    perc_3d = Percolation_3D()
    perc_3d.start_sampling()
