'''
build a second map representing the distance to traverse each point
    1 for regular cells
    1M for cells in empty rows/cols
build list of locations of galaxies
compute and sum distances between pairs of galaxies by summing values between points
'''
import numpy as np


def go(lines, empty_space_distance):
    arr = np.array(lines, dtype=str)
    arr_distance = np.ones(arr.shape, dtype=int)
    empty_rows = np.sum(arr == '#', axis=1) == 0
    arr_distance[empty_rows, :] = empty_space_distance
    empty_cols = np.sum(arr == '#', axis=0) == 0
    arr_distance[:, empty_cols] = empty_space_distance
    galaxy_coords = np.nonzero(arr == '#')
    galaxy_coords = list(zip(galaxy_coords[0], galaxy_coords[1]))

    total = 0
    for galaxy_index_1 in range(0, len(galaxy_coords)-1):
        for galaxy_index_2 in range(galaxy_index_1+1, len(galaxy_coords)):
            row_1, col_1 = galaxy_coords[galaxy_index_1]
            row_2, col_2 = galaxy_coords[galaxy_index_2]
            first_row, last_row = min(row_1, row_2), max(row_1, row_2)
            first_col, last_col = min(col_1, col_2), max(col_1, col_2)
            row_distance = np.sum(arr_distance[first_row + 1:last_row + 1, first_col])
            col_distance = np.sum(arr_distance[first_row, first_col + 1:last_col + 1])
            shortest_distance = row_distance + col_distance
            total += shortest_distance
    print(total)


with open('day11.txt', 'rt') as f:
    lines = [list(line.strip()) for line in f.readlines()]
go(lines, 2)
go(lines, 1000000)
