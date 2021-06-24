from pprint import pprint
from math import sqrt
from copy import deepcopy
from misc import time_it, flatten_once, find_shape


def find_path_2D(lattice, start=None, end=None, pathing=False):
    """
    always tries to find path from top left to bottom right [0,0] > [max_x,max_y]
    Tries to imitate A* pathfinding; only adjacent cells are checked

    :param lattice: a lattice to find path through
    :param start: point at algorithm starts from, defaults at (0, 0)
    :param end: point to reach, default is (len(lattice), len(lattice_row))
    :param pathing: keep the information about point-to-point path from start to end
    :return: True/False value, whether a path between points exist
    """
    if start is None:
        start = [0, 0]
    if end is None:
        end = [len(lattice[0]), len(lattice)]

    max_x: int = end[0]
    max_y: int = end[1]
    pos = start
    visited = [start]
    route = [start]
    possible = []

    while pos != [max_y - 1, max_x - 1]:
        # north/south (up/down), west/east (left/right) order
        dist_n, dist_s, dist_w, dist_e = -1, -1, -1, -1

        # test surroundings
        # False value immediately causes expression to equal 0, subtracting -0.001 causes it to be viable
        # for < 0 checks
        if pos[0] > 0:
            dist_n = sqrt((max_x - (pos[0] - 1)) ** 2 + (max_y - pos[1]) ** 2) * int(
                lattice[pos[0] - 1][pos[1]]) - 0.001
        if pos[0] < max_y - 1:
            dist_s = sqrt((max_x - (pos[0] + 1)) ** 2 + (max_y - pos[1]) ** 2) * int(
                lattice[pos[0] + 1][pos[1]]) - 0.001
        if pos[1] > 0:
            dist_w = sqrt((max_x - pos[0]) ** 2 + (max_y - (pos[1] - 1)) ** 2) * int(
                lattice[pos[0]][pos[1] - 1]) - 0.001
        if pos[1] < max_x - 1:
            dist_e = sqrt((max_x - pos[0]) ** 2 + (max_y - (pos[1] + 1)) ** 2) * int(
                lattice[pos[0]][pos[1] + 1]) - 0.001

        # check adjacent (later - a) cells for illogical distances and sort them in order of distance from end
        d = [_ for _ in [
            [[pos[0] - 1, pos[1]], dist_n],
            [[pos[0] + 1, pos[1]], dist_s],
            [[pos[0], pos[1] - 1], dist_w],
            [[pos[0], pos[1] + 1], dist_e]
        ] if _[1] > 0]

        d = sorted(d, key=lambda a: a[1])
        x, selected, changed = 0, 0, False
        while x < len(d):
            if d[x][0] not in visited:
                if not changed:
                    selected, changed = x, True
                elif pathing:
                    # without deepcopy, weird things get appended and we get undesired behaviour
                    r = deepcopy(route)
                    r.append(d[x][0])
                    possible.append(r)
                else:
                    possible.append(d[x][0])
            x += 1

        if changed:
            visited.append(pos)
            pos = d[selected][0]
            if pathing:
                route.append(d[selected][0])
        else:
            try:
                if pathing:
                    route = possible.pop()
                    pos = route[-1]
                else:
                    pos = possible.pop()
            except IndexError:
                return False

    return True


def find_path_3D(lattice, start=None, end=None, pathing=False):
    """
    exact same algorithm as find_path_2D, however one that is designed for 3 dimensional space

    :param lattice: 3D array to look through
    :param start: a lattice starting point for algorithm
    :param end: point we try to get to
    :param pathing: keep the information about point-to-point path from start to end
    :return: True/False value, whether a path between points exist
    """
    if start is None:
        start = [0, 0, 0]
    if end is None:
        end = [len(lattice[0][0]), len(lattice[0]), len(lattice)]

    max_x: int = end[0]
    max_y: int = end[1]
    max_z: int = end[2]

    pos = start
    visited = [start]
    route = [start]
    possible = []

    steps = 0
    while pos != [max_z - 1, max_y - 1, max_x - 1] and steps < 300:
        steps += 1
        # north/south, west/east, back/front order
        dist_n, dist_s, dist_w, dist_e, dist_b, dist_f = -1, -1, -1, -1, -1, -1

        if pos[0] > 0:
            dist_n = sqrt(
                (max_x - (pos[0] - 1)) ** 2 +
                (max_y - pos[1]) ** 2 +
                (max_z - pos[2]) ** 2) * int(lattice[pos[0] - 1][pos[1]][pos[2]]) - 0.001
        if pos[0] < max_z - 1:
            dist_s = sqrt(
                (max_x - (pos[0] + 1)) ** 2 +
                (max_y - pos[1]) ** 2 +
                (max_z - pos[2]) ** 2) * int(lattice[pos[0] + 1][pos[1]][pos[2]]) - 0.001
        if pos[1] > 0:
            dist_w = sqrt(
                (max_x - pos[0]) ** 2 +
                (max_y - (pos[1] - 1)) ** 2 +
                (max_z - pos[2]) ** 2) * int(lattice[pos[0]][pos[1] - 1][pos[2]]) - 0.001
        if pos[1] < max_y - 1:
            dist_e = sqrt(
                (max_x - pos[0]) ** 2 +
                (max_y - (pos[1] + 1)) ** 2 +
                (max_z - pos[2]) ** 2) * int(lattice[pos[0]][pos[1] + 1][pos[2]]) - 0.001
        if pos[2] > 0:
            dist_b = sqrt(
                (max_x - pos[0]) ** 2 +
                (max_y - pos[1]) ** 2 +
                (max_z - (pos[2] - 1)) ** 2) * int(lattice[pos[0]][pos[1]][pos[2] - 1]) - 0.001
        if pos[2] < max_x - 1:
            dist_f = sqrt(
                (max_x - pos[0]) ** 2 +
                (max_y - pos[1]) ** 2 +
                (max_z - (pos[2] + 1)) ** 2) * int(lattice[pos[0]][pos[1]][pos[2] + 1]) - 0.001

        d = [_ for _ in [
            [[pos[0] - 1, pos[1], pos[2]], dist_n],
            [[pos[0] + 1, pos[1], pos[2]], dist_s],
            [[pos[0], pos[1] - 1, pos[2]], dist_w],
            [[pos[0], pos[1] + 1, pos[2]], dist_e],
            [[pos[0], pos[1], pos[2] - 1], dist_b],
            [[pos[0], pos[1], pos[2] + 1], dist_f]
        ] if _[1] > 0]

        d = sorted(d, key=lambda a: a[1])
        x, selected, changed = 0, 0, False
        while x < len(d):
            if d[x][0] not in visited:
                if not changed:
                    selected, changed = x, True
                elif pathing:
                    r = deepcopy(route)
                    r.append(d[x][0])
                    possible.append(r)
                else:
                    possible.append(d[x][0])
            x += 1

        if changed:
            visited.append(pos)
            pos = d[selected][0]
            if pathing:
                route.append(d[selected][0])
        else:
            try:
                if pathing:
                    route = possible.pop()
                    pos = route[-1]
                else:
                    pos = possible.pop()
            except IndexError:
                return False

    return True


class DistanceMap:
    def __init__(self, lattice, shape=None, start=None, end=None):
        """
        creates a map of distances, that can be used to evaluate path choices for algorithm, instead of calculating all
        adjacent cell distances ever step and choosing right one then

        the main incentive for this is to flatten the lattice and compute entire list in one go, possibly even
        accelerating the process by multithreading it with the use of either CPU or GPU
        :param lattice: data with cells for algorithm
        :param shape: shape of matrix/array/lattice
        :param start: starting point of algorithm
        :param end: end point " == "
        """
        self._lattice = lattice
        if shape is None:
            (self._dimensions,
             self._shape,
             self._flattened) = find_shape(lattice)
        else:
            (self._dimensions,
             self._shape) = len(shape), shape
            self._flattened = flatten_once(self._lattice)
            for i in range(self._dimensions-1):
                self._flattened = flatten_once(self._flattened)
        if start is None:
            self._start = [0 for _ in range(self._dimensions)]
        else:
            self._start = start

        if end is None:
            self._end = [_-1 for _ in self._shape]
        else:
            self._end = end

        for l in self._lattice:
            print(l)
        print(self._dimensions, self._shape, self._start, self._end, self._flattened)
        self._map = self.create_map()

    @time_it
    def create_map(self):
        """
        create map used flattened array, coordinates of points that represented particular position in flattened array were
        obtained by dividing index by a certain multiplier with casting into int(), once for each dimension into _[0], with
        reminder saved to _[1] memory to be used in next iteration.

        Since distance is created by square root of sum of squared differences between end and start,
        sum of each squared difference is accumulated and root calculated in last step. This approach is
        universal and can be scaled into any number of dimensions without changing the core of algorithm.
        :return:
        """
        m = [[0, _[1]] for _ in enumerate(range(len(self._flattened)))]
        multipliers = [self._shape[0]]
        for s in self._shape[1:]:
            multipliers.append(multipliers[-1] * s)
        multipliers.pop()
        multipliers = multipliers[::-1]
        f = list(enumerate(multipliers))
        e = self._end[::-1]
        for i in range(len(e)-1):
            m = [[
                j[0] + (e[i] - int(j[1] / f[i][1]))**2,
                j[1] - (int(j[1] / f[i][1])) * f[i][1]]
                    for j in m]
        m = [_[0] + (e[2] - _[1])**2 for _ in m]
        return [sqrt(_) for _ in m]

    @time_it
    def create_map_traditional(self):
        """
        create map 'traditional' used nested loop-in-loop structure with 3 iterators
        only works with 3 dimensions, no more, no less

        i can see a probable solution of making a "string prototype" of the 'tradtional code' of the function, that would
        append a string representation of another iterator for every other dimension. Then in python there exist an
        exec() i could pass this string to and we get dimension-scaling solution, however i can't think of a way to
        multithread such weird approach
        :return:
        """
        m = []
        e = self._end[::-1]
        if self._dimensions == 3:
            for i in range(len(self._lattice)):
                for j in range(len(self._lattice[0])):
                    for k in range(len(self._lattice[0][0])):
                        m.append(
                            sqrt(
                                (e[0]-i)**2
                                +(e[1]-j)**2
                                +(e[2]-k)**2
                            )
                        )
        return m

    def show_map(self):
        pprint(self._map)

    def get_map(self):
        return self._map


if __name__ == '__main__':
    from random import seed
    from percolation import (
        lattice_gen_2D as lat_2d,
        lattice_gen_3D as lat_3d
    )

    # test against known case
    seed(200)
    # no possible path
    l_2d = [[True] + line + [True] for line in lat_2d()]
    # guaranteed path
    l_2d_2 = [[True] + line + [True] for line in lat_2d(p=0.7)]

    assert not time_it(find_path_2D)(l_2d)
    assert time_it(find_path_2D)(l_2d_2)

    # no possible path
    l_3d = [[[True] + line + [True] for line in surface]
            for surface in lat_3d()]
    # guaranteed path with use of 3 dimensions
    l_3d_2 = [[[True] + line + [True] for line in surface]
              for surface in lat_3d(p=0.4)]

    assert not time_it(find_path_3D)(l_3d)
    assert time_it(find_path_3D)(l_3d_2)
    # print_lat_3d(l_3d_2)
    d_map = DistanceMap(lattice=l_3d)
    m1 = d_map.get_map()
    m2 = d_map.create_map_traditional()
    # pprint(m2)
    assert m1 == m2
