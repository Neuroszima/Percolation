from math import sqrt
from copy import deepcopy


def find_path_2D(surface, start=None, end=None):
    """
    always tries to find path from top left to bottom right [0,0] > [max_x,max_y]
    Tries to imitate A* pathfinding,

    :param surface: a lattice to find path through
    :param start: point at algorithm starts from, defaults at (0, 0)
    :param end: point to reach, default is (len(lattice), len(lattice_row))
    :return:
    """
    if start is None:
        start = [0, 0]
    if end is None:
        end = [len(surface[0]), len(surface)]

    max_x: int = end[0]
    max_y: int = end[1]
    pos = start
    visited = [start]
    route = [start]
    possible = []

    step = 0
    while pos != [max_y-1, max_x-1]:
        step += 1
        dist_n, dist_s, dist_w, dist_e = -1, -1, -1, -1
        # test surroundings
        if pos[0] > 0:
            dist_n = sqrt((max_x-(pos[0]-1))**2 + (max_y-pos[1])**2) * int(surface[pos[0]-1][pos[1]]) - 0.001
        if pos[0] < max_y-1:
            dist_s = sqrt((max_x-(pos[0]+1))**2 + (max_y-pos[1])**2) * int(surface[pos[0]+1][pos[1]]) - 0.001
        if pos[1] > 0:
            dist_w = sqrt((max_x-pos[0])**2 + (max_y-(pos[1]-1))**2) * int(surface[pos[0]][pos[1]-1]) - 0.001
        if pos[1] < max_x-1:
            dist_e = sqrt((max_x-pos[0])**2 + (max_y-(pos[1]+1))**2) * int(surface[pos[0]][pos[1]+1]) - 0.001

        d = [_ for _ in [
            [[pos[0]-1, pos[1]], dist_n],
            [[pos[0]+1, pos[1]], dist_s],
            [[pos[0], pos[1]-1], dist_w],
            [[pos[0], pos[1]+1], dist_e]
        ] if _[1] > 0]

        d = sorted(d, key=lambda s: s[1])
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
