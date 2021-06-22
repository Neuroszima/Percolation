from math import sqrt
from copy import deepcopy


def find_path_2D(lattice, start=None, end=None):
    """
    always tries to find path from top left to bottom right [0,0] > [max_x,max_y]
    Tries to imitate A* pathfinding,

    :param lattice: a lattice to find path through
    :param start: point at algorithm starts from, defaults at (0, 0)
    :param end: point to reach, default is (len(lattice), len(lattice_row))
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

    while pos != [max_y-1, max_x-1]:
        # north/south (up/down), west/east (left/right) order
        dist_n, dist_s, dist_w, dist_e = -1, -1, -1, -1

        # test surroundings
        # False value immidietaly causes expression to equal 0, substracting -0.001 causes it to be viable
        # for < 0 checks
        if pos[0] > 0:
            dist_n = sqrt((max_x-(pos[0]-1))**2 + (max_y-pos[1])**2) * int(lattice[pos[0] - 1][pos[1]]) - 0.001
        if pos[0] < max_y-1:
            dist_s = sqrt((max_x-(pos[0]+1))**2 + (max_y-pos[1])**2) * int(lattice[pos[0] + 1][pos[1]]) - 0.001
        if pos[1] > 0:
            dist_w = sqrt((max_x-pos[0])**2 + (max_y-(pos[1]-1))**2) * int(lattice[pos[0]][pos[1] - 1]) - 0.001
        if pos[1] < max_x-1:
            dist_e = sqrt((max_x-pos[0])**2 + (max_y-(pos[1]+1))**2) * int(lattice[pos[0]][pos[1] + 1]) - 0.001

        # check adjacent (later - a) cells for illogical distances and sort them in order of distance from end
        d = [_ for _ in [
            [[pos[0]-1, pos[1]], dist_n],
            [[pos[0]+1, pos[1]], dist_s],
            [[pos[0], pos[1]-1], dist_w],
            [[pos[0], pos[1]+1], dist_e]
        ] if _[1] > 0]

        d = sorted(d, key=lambda a: a[1])
        x, selected, changed = 0, 0, False
        while x < len(d):
            if d[x][0] not in visited:
                if not changed:
                    selected, changed = x, True
                elif changed:
                    r = deepcopy(route)
                    r.append(d[x][0])
                    possible.append(r)
            x += 1

        if changed:
            route.append(d[selected][0])
            visited.append(pos)
            pos = d[selected][0]
        else:
            try:
                route = possible.pop()
                pos = route[-1]
            except IndexError:
                return False

    return True


def find_path_3D(lattice, start=None, end=None, verbose=False):
    """
    exact same algorithm as above, however one that is designed for 3 dimensional space

    :param lattice: 3D array to look through
    :param start: a lattice starting point for algorithm
    :param end: point we try to get to
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
    while pos != [max_z-1, max_y-1, max_x-1] and steps < 300:
        steps += 1
        # north/south, west/east, back/front order
        dist_n, dist_s, dist_w, dist_e, dist_b, dist_f = -1, -1, -1, -1, -1, -1

        if pos[0] > 0:
            dist_n = sqrt(
                (max_x - (pos[0]-1))**2 +
                (max_y - pos[1])**2 +
                (max_z - pos[2])**2) * int(lattice[pos[0] - 1][pos[1]][pos[2]]) - 0.001
        if pos[0] < max_z-1:
            dist_s = sqrt(
                (max_x - (pos[0] + 1))**2 +
                (max_y - pos[1])**2 +
                (max_z - pos[2])**2) * int(lattice[pos[0] + 1][pos[1]][pos[2]]) - 0.001
        if pos[1] > 0:
            dist_w = sqrt(
                (max_x - pos[0])**2 +
                (max_y - (pos[1]-1))**2 +
                (max_z - pos[2])**2) * int(lattice[pos[0]][pos[1] - 1][pos[2]]) - 0.001
        if pos[1] < max_y - 1:
            dist_e = sqrt(
                (max_x - pos[0])**2 +
                (max_y - (pos[1]+1))**2 +
                (max_z - pos[2])**2) * int(lattice[pos[0]][pos[1] + 1][pos[2]]) - 0.001
        if pos[2] > 0:
            dist_b = sqrt(
                (max_x - pos[0])**2 +
                (max_y - pos[1])**2 +
                (max_z - (pos[2]-1))**2) * int(lattice[pos[0]][pos[1]][pos[2] - 1]) - 0.001
        if pos[2] < max_x - 1:
            dist_f = sqrt(
                (max_x - pos[0])**2 +
                (max_y - pos[1])**2 +
                (max_z - (pos[2]+1))**2) * int(lattice[pos[0]][pos[1]][pos[2] + 1]) - 0.001

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
                elif changed:
                    r = deepcopy(route)
                    r.append(d[x][0])
                    possible.append(r)
            x += 1

        if changed:
            route.append(d[selected][0])
            visited.append(pos)
            pos = d[selected][0]
            # print(f"step {steps}, route: {route}, \nvisited: {len(visited)}\n" +
            #       f"other routes: {len(possible)}")
        else:
            try:
                route = possible.pop()
                pos = route[-1]
            except IndexError:
                return False

    return True


def print_lat_3d(lat):
    print("3d lattice")
    for surface in lat:
        for line in surface:
            print(line)
        print('\n')


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
    l_2d_2 = [[True] + line + [True] for line in lat_2d(p = 0.7)]

    assert (find_path_2D(l_2d)) == False
    assert (find_path_2D(l_2d_2)) == True

    # no possible path
    l_3d = [[[True] + line + [True] for line in surface]
              for surface in lat_3d()]
    # guaranteed path with use of 3 dimensions
    l_3d_2 = [[[True] + line + [True] for line in surface]
              for surface in lat_3d(p = 0.4)]

    assert find_path_3D(l_3d) == False
    assert find_path_3D(l_3d_2) == True

    print_lat_3d(l_3d_2)
