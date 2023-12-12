import numpy as np


def pretty_print(nd_arr):
    lines = nd_arr.tolist()
    for line in lines:
        s = ''
        for element in line:
            if type(element) == bool:
                element = str(element)[0]
            elif type(element) == int:
                element = f'{element:8d}'
            s += str(element)
        print(s)


def part_1(lines):
    '''
    insert extra rows/cols into array before empty rows/cols
    build list of locations of galaxies
    compute and sum distances between pairs of galaxies
    '''
    arr = np.array(lines, dtype=str)
    empty_rows = np.sum(arr == '#', axis=1) == 0
    arr = np.insert(arr, *np.nonzero(empty_rows), '.', axis=0)
    empty_cols = np.sum(arr == '#', axis=0) == 0
    arr = np.insert(arr, *np.nonzero(empty_cols), '.', axis=1)
    galaxy_coords = np.nonzero(arr == '#')
    galaxy_coords = list(zip(galaxy_coords[0], galaxy_coords[1]))

    total = 0
    for galaxy_index_1 in range(0, len(galaxy_coords)-1):
        for galaxy_index_2 in range(galaxy_index_1+1, len(galaxy_coords)):
            row_distance, col_distance = np.abs(np.array(galaxy_coords[galaxy_index_1]) - np.array(galaxy_coords[galaxy_index_2]))
            total += row_distance + col_distance
    print(total)


def part_2(lines):
    '''
    build a second map representing the distance to traverse that point
        1 for regular cells
        1M for cells in empty rows/cols
    build list of locations of galaxies
    compute and sum distances between pairs of galaxies by summing values between points
    '''
    EMPTY_SPACE_DISTANCE = 1000000
    arr = np.array(lines, dtype=str)
    arr_distance = np.ones((arr.shape), dtype=int)
    empty_rows = np.sum(arr == '#', axis=1) == 0
    arr_distance[empty_rows, :] = EMPTY_SPACE_DISTANCE
    empty_cols = np.sum(arr == '#', axis=0) == 0
    arr_distance[:, empty_cols] = EMPTY_SPACE_DISTANCE
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
part_1(lines)
part_2(lines)