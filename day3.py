'''
part 1

read the input into a numpy ndarray arr_1
pad arr_1 with '_' by maximum possible size of part number (np.pad)
create boolean value mask mask_is_number indicating location of numbers
create boolean value mask m_1 indicating location of symbols
create boolean value mask mask_is_symbol_adjacent indicating location of cells adjacent to symbols
create mask m_actual of numbers (mask_is_number) that are overlapped by mask_is_symbol_adjacent

add m_actual to mask_part_number
while m_actual isn't empty
  create mask m_possible by shifting mask m_actual one to the left (np.roll)
  create mask m_actual of numbers (mask_is_number) that are overlapped by m_possible
  add m_actual to mask_part_number

do same thing again (starting from mask m_actual of numbers (mask_is_number) that are overlapped by mask_isSymbolAdjacent), but shift right

convert rows of m_partnums to strings
split strings by spaces to get numbers
sum numbers
'''

'''
part 2

for each * symbol on the board
    create a new version of the board with just that one * symbol, and all the numbers
    modify part 1 to count the number of numbers left on the board when non-adjacent numbers are removed
    for symbols with 2 numbers remaining on the board, calculate their product and sum the products
'''

import numpy as np


def print_ndarray(arr):
    for x in arr.tolist():
        for y in x:
            if arr.dtype == 'bool':
                if y:
                    print('X', sep=' ', end='')
                else:
                    print('_', sep=' ', end='')
            else:
                print(y, sep=' ', end='')
        print()


def find_part_numbers(arr_1):

    keep_numbers = np.frompyfunc(lambda x: x if '0' <= x <= '9' else ' ', 1, 1)
    arr_numbers = keep_numbers(arr_1)
    mask_is_number = arr_numbers != ' '

    mask_temp1 = (('0' > arr_1) | (arr_1 > '9')) & (arr_1 != '_') & (arr_1 != '.') & (arr_1 != ' ')
    mask_temp2 = np.roll(mask_temp1, 1, axis=0) | np.roll(mask_temp1, -1, axis=0)
    mask_temp3 = np.roll(mask_temp2, 1, axis=1) | np.roll(mask_temp2, -1, axis=1)
    mask_is_symbol_adjacent = mask_temp2 | mask_temp3 | np.roll(mask_temp1, 1, axis=1) | np.roll(mask_temp1, -1, axis=1)

    m_actual = mask_is_symbol_adjacent & mask_is_number
    mask_part_number = m_actual
    # add positions to the left of m_actual that contain numbers to mask_part_number
    while m_actual.sum() > 0:
        m_possible = np.roll(m_actual, -1, axis=1)
        m_actual = m_possible & mask_is_number
        mask_part_number = mask_part_number | m_actual

    m_actual = mask_is_symbol_adjacent & mask_is_number
    # add positions to the right of m_actual that contain numbers to mask_part_number
    while m_actual.sum() > 0:
        m_possible = np.roll(m_actual, 1, axis=1)
        m_actual = m_possible & mask_is_number
        mask_part_number = mask_part_number | m_actual

    arr_numbers[mask_part_number == False] = ' '

    total = 0
    count = 0
    product = 0
    for line in arr_numbers.tolist():
        x1 = ''.join(line).strip()
        nums = str(x1).split(' ')
        for y in nums:
            y1 = y.strip()
            if y1 != '':
                total += int(y1)
                count += 1
                if product == 0:
                    product = int(y1)
                else:
                    product *= int(y1)

    return count, total, product


np.set_printoptions(threshold=10000, linewidth=100000)

with open('day3.txt', 'rt') as f:
    lines = [list(line.strip()) for line in f.readlines()]

arr_1 = np.array(lines)
arr_1 = np.pad(arr_1, pad_width=1, mode='constant', constant_values='_')

# part 1
_, total, _ = find_part_numbers(arr_1)
print(f'total: {total}')

# part 2
# find all of the * symbols
star_symbols = np.nonzero(arr_1 == '*')
star_symbols = [(row, col) for row, col in zip(star_symbols[0], star_symbols[1])]
keep_numbers = np.frompyfunc(lambda x: x if '0' <= x <= '9' else ' ', 1, 1)
arr_numbers = keep_numbers(arr_1)

# add one * symbol to the number array at a time and check the product of adjacent numbers
total = 0
for star_symbol in star_symbols:
    # add star_symbol to number array
    arr_numbers[star_symbol] = '*'
    count, _, product = find_part_numbers(arr_numbers)
    if count == 2:
        total += product
    # remove star_symbol from number array
    arr_numbers[star_symbol] = ' '
print(f'total: {total}')
