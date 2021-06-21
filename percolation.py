from random import random
from pathfinding import find_path_2D


def lattice_gen_2D(x=10, y=10, p=0.1):
    return [[True if random() < p else False for _ in range(x)]
            for _ in range(y)]


def lattice_gen_3D(x=10, y=10, z=10, p=0.1):
    return [[[True if random() < p else False for _ in range(x)]
             for _ in range(y)]
             for _ in range(z)]


if __name__ == "__main__":
    #warning, program runs for a lot of tmie!

    data = []
    propabilities = [0.1 + 0.02 * _ for _ in range(5, 25)]
    sizes = list(range(4, 14))
    samples_per_size = 100

    #2 dimensional lattice
    for size in sizes:
        size_set = []
        for pr in propabilities:
            prop_data = 0
            for i in range(samples_per_size):
                lat = lattice_gen_2D(size, size, pr)
                #horizontal test
                if find_path_2D([[True] + line + [True] for line in lat]): prop_data+=1
            size_set.append(prop_data)
        data.append(size_set)

    #printing results
    for size, data_row in zip(sizes, data):
        for pr, counts in zip(propabilities, data_row):
            print(f"size: {size}, prop: {pr}, counts:{counts}")
