import math

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def get_first_and_last(line, include_number_strings=False):
    line = line.strip()

    first_num_pos = math.inf
    first_num = None
    last_num_pos = -math.inf
    last_num = None

    for i in range(len(line)):
        for num_i, number in enumerate(numbers):
            if num_i > 9 and not include_number_strings:
                break
            pos = line.find(number, i, len(line))
            if pos >= 0:
                if 0 <= pos < first_num_pos:
                    first_num_pos = pos
                    first_num = num_i % 10
                if last_num_pos < pos >= 0:
                    last_num_pos = pos
                    last_num = num_i % 10

    return first_num, last_num


for include_number_strings in [False, True]:
    sum = 0
    with (open('day1.txt', 'rt') as f):
        line = f.readline()
        while line != '':
            first, last = get_first_and_last(line, include_number_strings=include_number_strings)
            sum += first * 10 + last
            line = f.readline()
    print(sum)