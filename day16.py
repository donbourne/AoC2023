import numpy as np
from collections import namedtuple
from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


MOVE_UP = np.array([-1, 0])
MOVE_DOWN = np.array([1, 0])
MOVE_RIGHT = np.array([0, 1])
MOVE_LEFT = np.array([0, -1])


delta_and_direction = {
    ('.', Direction.UP): [(np.array(MOVE_UP), Direction.UP)],
    ('.', Direction.DOWN): [(np.array(MOVE_DOWN), Direction.DOWN)],
    ('.', Direction.RIGHT): [(np.array(MOVE_RIGHT), Direction.RIGHT)],
    ('.', Direction.LEFT): [(np.array(MOVE_LEFT), Direction.LEFT)],

    ('-', Direction.UP): [(np.array(MOVE_LEFT), Direction.LEFT), (np.array(MOVE_RIGHT), Direction.RIGHT)],
    ('-', Direction.DOWN): [(np.array(MOVE_LEFT), Direction.LEFT), (np.array(MOVE_RIGHT), Direction.RIGHT)],
    ('-', Direction.RIGHT): [(np.array(MOVE_RIGHT), Direction.RIGHT)],
    ('-', Direction.LEFT): [(np.array(MOVE_LEFT), Direction.LEFT)],

    ('|', Direction.UP): [(np.array(MOVE_UP), Direction.UP)],
    ('|', Direction.DOWN): [(np.array(MOVE_DOWN), Direction.DOWN)],
    ('|', Direction.RIGHT): [(np.array(MOVE_UP), Direction.UP), (np.array(MOVE_DOWN), Direction.DOWN)],
    ('|', Direction.LEFT): [(np.array(MOVE_UP), Direction.UP), (np.array(MOVE_DOWN), Direction.DOWN)],

    ('/', Direction.UP): [(np.array(MOVE_RIGHT), Direction.RIGHT)],
    ('/', Direction.DOWN): [(np.array(MOVE_LEFT), Direction.LEFT)],
    ('/', Direction.RIGHT): [(np.array(MOVE_UP), Direction.UP)],
    ('/', Direction.LEFT): [(np.array(MOVE_DOWN), Direction.DOWN)],

    ('\\', Direction.UP): [(np.array(MOVE_LEFT), Direction.LEFT)],
    ('\\', Direction.DOWN): [(np.array(MOVE_RIGHT), Direction.RIGHT)],
    ('\\', Direction.RIGHT): [(np.array(MOVE_DOWN), Direction.DOWN)],
    ('\\', Direction.LEFT): [(np.array(MOVE_UP), Direction.UP)]
}


def is_valid_position(position):
    return 0 <= position[0] < input_map.shape[0] and 0 <= position[1] < input_map.shape[1]


def get_next_beam_heads(energized_map, beam_head, symbol):
    possible_delta_and_direction = delta_and_direction[(symbol, beam_head.direction)]

    # filter list down to ones that are within the bounds of the input_map
    valid_delta_and_direction = [d for d in possible_delta_and_direction if is_valid_position(tuple(beam_head.position + d[0]))]

    # keep options that haven't been seen before
    next_beam_heads=[]
    for position, direction in valid_delta_and_direction:
        new_position = beam_head.position + position
        if energized_map[direction.value][tuple(new_position)] != 1:
            next_beam_heads.append(BeamHead(position=new_position, direction=direction))
            energized_map[direction.value][tuple(new_position)] = 1

    return next_beam_heads


def compute_energized(energized_map, beam_heads):

    while len(beam_heads) > 0:
        beam_head = beam_heads.pop()
        next_beam_heads = get_next_beam_heads(energized_map, beam_head, input_map[tuple(beam_head.position)])
        beam_heads.extend(next_beam_heads)


def part_1():
    energized_map = [np.zeros(input_map.shape, dtype=int) for _ in range(0,4)]
    energized_map[Direction.RIGHT.value][0,0] = 1
    beam_heads = [BeamHead(np.array([0, 0]), Direction.RIGHT)]
    compute_energized(energized_map, beam_heads)
    print(np.sum(energized_map[0] | energized_map[1] | energized_map[2] | energized_map[3]))


def find_most_energized_state(row_range, col_range, start_direction):
    max_energized = 0

    for row in row_range:
        for col in col_range:
            energized_map = [np.zeros(input_map.shape, dtype=int) for _ in range(0, 4)]
            energized_map[start_direction.value][row, col] = 1
            beam_heads = [BeamHead(np.array([row, col]), start_direction)]
            compute_energized(energized_map, beam_heads)
            energized = np.sum(energized_map[0] | energized_map[1] | energized_map[2] | energized_map[3])
            if energized > max_energized:
                max_energized = energized

    return max_energized


def part_2():
    max_energized = 0

    # left side
    row_range = range(0, input_map.shape[0])
    col_range = range(0, 1)
    start_direction = Direction.RIGHT
    energized = find_most_energized_state(row_range, col_range, start_direction)
    if energized > max_energized:
        max_energized = energized

    # right side
    row_range = range(0, input_map.shape[0])
    col_range = range(input_map.shape[1]-1, input_map.shape[1])
    start_direction = Direction.LEFT
    energized = find_most_energized_state(row_range, col_range, start_direction)
    if energized > max_energized:
        max_energized = energized

    # top side
    row_range = range(0, 1)
    col_range = range(0, input_map.shape[1])
    start_direction = Direction.DOWN
    energized = find_most_energized_state(row_range, col_range, start_direction)
    if energized > max_energized:
        max_energized = energized

    # bottom side
    row_range = range(input_map.shape[0]-1, input_map.shape[0])
    col_range = range(0, input_map.shape[1])
    start_direction = Direction.UP
    energized = find_most_energized_state(row_range, col_range, start_direction)
    if energized > max_energized:
        max_energized = energized

    print(max_energized)


with open('day16.txt', 'rt') as f:
    input_map = np.array([list(line.strip()) for line in f.readlines()])

energized_map = []
BeamHead = namedtuple('BeamHead', ['position', 'direction'])

part_1()
part_2()