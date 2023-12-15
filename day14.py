import numpy as np
import re
from enum import Enum


def check_load(arr):
    multipliers = np.arange(arr.shape[0], 0, -1)
    # print(multipliers)
    count = np.sum(arr == 'O', axis=1)
    # print(count)
    load = count * multipliers
    # print(load)
    load = np.sum(load)
    return load


class Direction(Enum):
    WEST = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3


def tilt(nd_array, direction):
    # rotate the array so that the direction I'm going to tilt is pointed left (so I can use regex to do the tilt work)
    arr_rotated = np.rot90(nd_array, direction.value)
    # print(arr_rotated)
    lines_rotated = arr_rotated.tolist()
    strs_rotated = [''.join(line) for line in lines_rotated]
    # print(lines_rotated)
    strs_rolled = []
    for s in strs_rotated:
        done = False
        while not done:
            new_s = re.sub(r'(\.+)O', r'O\1', s)
            # print(f'{s}\n{new_s}\n')
            if s == new_s:
                done = True
                strs_rolled.append(new_s)
            else:
                s = new_s
    # print(strs_rolled)
    arr = np.array([list(s) for s in strs_rolled])
    arr = np.rot90(arr, -direction.value)
    return arr


def part_1(lines):
    arr = np.array(lines)
    # print(arr)
    arr = tilt(arr, Direction.NORTH)
    # print(arr)
    load = check_load(arr)
    print(load)


def part_2(lines):
    arr = np.array(lines)
    # print(arr)
    layouts = []
    layouts_map = {}

    done = False
    cycles = 0
    while not done:
        # rotate clockwise 4 times then check load
        arr = tilt(arr, Direction.NORTH)
        # print(arr, '\n')
        arr = tilt(arr, Direction.WEST)
        # print(arr, '\n')
        arr = tilt(arr, Direction.SOUTH)
        # print(arr, '\n')
        arr = tilt(arr, Direction.EAST)
        cycles += 1
        # print(f'cycle {cycles} arr:\n{arr}')


        flat = arr.flatten().tostring()
        if flat in layouts:
            number_not_repeating = layouts.index(flat) + 1          # 10
            number_repeating = cycles - number_not_repeating        # 13 - 10 = 3
            # print(f'repeat of {layouts.index(flat)}')
            done = True
        else:
            layouts.append(flat)
            layouts_map[flat] = arr

    num_cycles = 1000000000
    # print(len(layouts_map))
    end_state = number_not_repeating + ((num_cycles - number_not_repeating) % number_repeating)     # 10 + (24-10) % 3 = 12
    end_layout = layouts_map[layouts[end_state-1]]
    # print(end_layout)
    end_load = check_load(end_layout)

    print(f'load: {end_load}')


with open('day14.txt', 'rt') as f:
    lines = [list(line.strip()) for line in f.readlines()]

part_1(lines)
part_2(lines)
