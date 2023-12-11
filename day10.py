'''
Part 1:
create a map symbol_to_delta for each of the symbols to a pair of delta row/cols of the next tiles
set 2 heads to the row,col coords of S
initialize prev_tile (None)
relabel S with the symbol it should have based on surrounding tiles
while heads aren't the same tile (other than on the first move)
    for each of the heads
        update head to the next tile
        update prev tile the current head

Part 2:

double the input map width and height by inserting rows/columns of #s
change loop following algorithm to insert | or -, as appropriate, when encountering #s
fill outside loop with X's, filling all adjacent tiles that aren't part of the loop
scale input map back down to normal size
enclosed area = total area - X area - loop area
'''
from collections import namedtuple

import numpy as np
import sys


def pretty_print(nd_arr):
    lines = nd_arr.tolist()
    for line in lines:
        s = ''
        for element in line:
            s += element
        print(s)


def s_to_symbol(s_coords):
    multiplier = part

    if np.isin(pipe_map[tuple(s_coords + UP * multiplier)], ['|', '7', 'F']):
        if np.isin(pipe_map[tuple(s_coords + RIGHT * multiplier)], ['-', 'J', '7']):
            return 'L'
        if np.isin(pipe_map[tuple(s_coords + DOWN * multiplier)], ['|', 'L', 'J']):
            return '|'
        if np.isin(pipe_map[tuple(s_coords + LEFT * multiplier)], ['-', 'L', 'F']):
            return 'J'
    if np.isin(pipe_map[tuple(s_coords + RIGHT * multiplier)], ['-', 'J', '7']):
        if np.isin(pipe_map[tuple(s_coords + DOWN * multiplier)], ['|', 'L', 'J']):
            return 'F'
        if np.isin(pipe_map[tuple(s_coords + LEFT * multiplier)], ['-', 'L', 'F']):
            return '-'
    if np.isin(pipe_map[tuple(s_coords + DOWN * multiplier)], ['|', 'L', 'J']):
        if np.isin(pipe_map[tuple(s_coords + LEFT * multiplier)], ['-', 'L', 'F']):
            return '7'
    else:
        print("could not find symbol for S")
        sys.exit()


def next_head(prev, head, symbol):
    possible_next_heads = head.coords + symbol_to_delta[symbol]
    possible_connectors = symbol_to_connector[symbol]
    possible = [Coord_Connector(head, connector) for head, connector in zip(possible_next_heads, possible_connectors)]
    next_heads = list(filter(lambda x: tuple(x.coords) != tuple(prev.coords), possible))
    return next_heads


def fill(coords, symbol, target_map):
    if target_map[tuple(coords)] != '':
        return

    explore = [coords]

    while len(explore) > 0:
        coords = explore.pop()

        if coords[0] >= 0 and coords[1] >= 0 and coords[0] <= (target_map.shape[0]-1) \
                and coords[1] <= (target_map.shape[1]-1) and target_map[tuple(coords)] == '':
            target_map[tuple(coords)] = symbol
            explore.extend([coords + UP, coords + LEFT, coords + RIGHT, coords + DOWN])


Coord_Connector = namedtuple('Coord_Connector', ['coords', 'connector'])

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])

symbol_to_delta = {
    '|': (UP, DOWN),
    '-': (LEFT, RIGHT),
    'L': (UP, RIGHT),
    'J': (UP, LEFT),
    '7': (LEFT, DOWN),
    'F': (RIGHT, DOWN)
}

symbol_to_connector = {
    '|': ('|', '|'),
    '-': ('-', '-'),
    'L': ('|', '-'),
    'J': ('|', '-'),
    '7': ('-', '|'),
    'F': ('-', '|')
}

np.set_printoptions(linewidth=600, formatter={'all': lambda x: f'{x:>1}'})
np.set_printoptions(threshold=sys.maxsize)

with open('day10.txt', 'rt') as f:
    lines = [list(line.strip()) for line in f.readlines()]

for part in [1,2]:
    pipe_map = np.array(lines)
    if part == 2:
        double_spaced_pipe_map = np.zeros((pipe_map.shape[0] * 2, pipe_map.shape[1] * 2), dtype='<U1')
        double_spaced_pipe_map[:] = '#'
        double_spaced_pipe_map[::2, ::2] = pipe_map
        pipe_map = double_spaced_pipe_map
        # pretty_print(pipe_map)
    if part == 2:
        loop_map = np.zeros(pipe_map.shape, dtype='<U1')            # a clean map with just the loop filled in

    s_loc = np.nonzero(pipe_map == 'S')         # returns a tuple with x coords in an array, y coords in an array
    s_coords = np.array((s_loc[0][0], s_loc[1][0]))
    if part == 2:
        loop_map[tuple(s_coords)] = 'L'                             # set all loop tiles to 'L'
    s_symbol = s_to_symbol(s_coords)

    heads = next_head(Coord_Connector((-1, -1), 'X'), Coord_Connector(s_coords, 'X'), s_symbol)
    prev_heads = [Coord_Connector(s_coords, 'X'), Coord_Connector(s_coords, 'X')]
    if part == 2:
        pipe_map[tuple(heads[0].coords)] = heads[0].connector       # set all spaces to appropriate connector
        pipe_map[tuple(heads[1].coords)] = heads[1].connector       # set all spaces to appropriate connector
        loop_map[tuple(heads[0].coords)] = 'L'                      # set all loop tiles to 'L'
        loop_map[tuple(heads[1].coords)] = 'L'                      # set all loop tiles to 'L'

    move_num = 1
    while tuple(heads[0].coords) != tuple(heads[1].coords):
        for i in [0, 1]:
            symbol = pipe_map[tuple(heads[i].coords)]
            tmp = heads[i]
            heads[i] = next_head(prev_heads[i], heads[i], symbol)[0]
            if part == 2:
                loop_map[tuple(heads[i].coords)] = 'L'              # set all loop tiles to 'L'
                if pipe_map[tuple(heads[i].coords)] == '#':
                    pipe_map[tuple(heads[i].coords)] = heads[i].connector   # set all spaces to appropriate connector
            prev_heads[i] = tmp
        move_num += 1

    if part == 1:
        print(move_num)

if part == 2:
    fill(np.array([0,0]), 'X', loop_map)


# shrink map back to normal size - remaining tiles in the map that haven't been filled in are the enclosed tiles
shrunk_map = loop_map[::2, ::2]
shrunk_map[shrunk_map == ''] = '_'
pretty_print(shrunk_map)

print((shrunk_map == '_').sum())