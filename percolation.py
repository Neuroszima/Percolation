from random import random, randint, uniform
from copy import deepcopy
from math import sqrt


def find_path(surface, start=None, max_step = 100):
    """
    always tries to find path from top left to bottom right [0,0] > [max_x,max_y]

    :param surface:
    :param start:
    :param end:
    :return:
    """
    if start is None:
        start = [0, 0]
    pos = start
    visited = [start]
    max_x = len(surface[0])
    max_y = len(surface)
    route = [start]
    possible = []
    distance = sqrt((max_x-start[0])**2 + (max_y-start[1])**2)

    step = 0
    command = "n"
    while pos != [max_y-1,max_x-1]:
        step += 1
        dist_n, dist_s, dist_w, dist_e = -1, -1, -1, -1
        #test surroundings
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
        known = [True if _[0] in visited else False for _ in d]
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
            distance = d[selected][1]
            visited.append(pos)
            pos = d[selected][0]
        else:
            try:
                route = possible.pop()
                pos = route[-1]
                distance = sqrt((pos[0] - start[0]) ** 2 + (pos[1] - start[1]) ** 2)
            except IndexError:
                return False

    return True

def lattice_gen(x=10, y=10, p=0.1):
    return [[True if random() < p else False for _ in range(x)]
            for _ in range(y)]


if __name__ == "__main__":
    #warning, program runs for a lot of tmie!

    data = []
    propabilities = [0.1 + 0.02 * _ for _ in range(5, 25)]
    sizes = list(range(5, 14))
    for size in sizes:
        size_set = []
        for pr in propabilities:
            prop_data = 0
            for i in range(200):
                lat = lattice_gen(size, size, pr)
                #horizontal
                lat = [[True] + line + [True] for line in lat]
                if find_path(lat): prop_data+=1
            size_set.append(prop_data)
        data.append(size_set)
    for size, data_row in zip(sizes, data):
        for pr, counts in zip(propabilities, data_row):
            print(f"size: {size}, prop: {pr}, counts:{counts}")