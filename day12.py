'''
part1

read the lines
for each line
    generate permutations of the line that convert ? chars to either # or .
    use regex to check which permutations are valid (increment total)
print total
'''
import math
import re

char_map={'0':'#', '1':'.'}

def criteria_to_regex(criteria):
    regex = r'^\.*'
    criteria = criteria.split(',')
    for i, c in enumerate(criteria):
        if i > 0:
            regex += r'\.+'
        regex += '#' * int(c)
    regex += r'\.*$'

    return regex


def generate_and_check_patterns(broken_pattern, criteria):
    criteria_re = criteria_to_regex(criteria)

    # count number of question marks
    num_question_marks = 0
    for c in broken_pattern:
        if c == '?':
            num_question_marks += 1

    # generate binary numbers that will be used to represent # or .
    valid_count = 0
    for i in range(0, int(math.pow(2, num_question_marks))):
        bin_i = f'{i:b}'.rjust(num_question_marks,'0')
        s = ''
        bin_i_index = 0
        for c in broken_pattern:
            if c == '?':
                s += char_map[bin_i[bin_i_index]]
                bin_i_index += 1
            else:
                s += c
        if re.search(criteria_re, s):
            valid_count += 1

    return valid_count


def part_1(lines):
    total = 0
    for line in lines:
        broken_pattern, criteria = line.split()
        count = generate_and_check_patterns(broken_pattern, criteria)
        # print(broken_pattern, criteria, count)
        total += count
    print(total)

'''
part 2

create a Part that represents one of the segments of the required sequence of .s and #s from the criteria
create a BlockPart (for the fixed length ### parts) and a SpacePart (for the variable length space parts)
create a list of Parts representing the criteria for the line 
check how long any space is allowed to get based on the minimum length of the Parts and the total length of the pattern
count valid permutations:
    memoize the number of permutations returned (keyed by part-number/position-in-pattern) from the following...
    walk from the first Part to the last, trying to place the Parts on the pattern to make sure they fit
        iterate over the number of spaces in each space Part
        add 1 to count when able to reach the end of the Parts having consumed the whole pattern
print the total count
'''

class Part:
    pass

class SpacePart(Part):
    def __init__(self, min_len):
        self.min_len = min_len
        self.is_space = True


class BlockPart(Part):
    def __init__(self, len):
        self.len = len
        self.is_space = False


def create_part_list(criteria):
    parts = []
    parts.append(SpacePart(0))
    criteria = criteria.split(',')
    for i, c in enumerate(criteria):
        if i > 0:
            parts.append(SpacePart(1))
        parts.append(BlockPart(int(c)))
    parts.append(SpacePart(0))

    return parts


def compute_max_space_len(broken_pattern, parts):
    # max number of spaces for any SpacePart will be the broken_pattern len minus sum of all
    # BlockPart sizes minus min len of all SpaceParts
    # plus 1 because already accounting for SpaceParts to have 1 space in len of SpaceParts
    broken_pattern_len = len(broken_pattern)
    sum_of_blockpart_lens = sum([part.len for part in parts if not part.is_space])
    sum_of_spacepart_lens = sum([part.min_len for part in parts if part.is_space])
    return broken_pattern_len - sum_of_blockpart_lens - sum_of_spacepart_lens + 1


def can_place(part, sub_broken_pattern):
    if part.is_space:
        if '#' in sub_broken_pattern[0:part.len]:
            return False
        else:
            return True
    elif '.' in sub_broken_pattern[0:part.len]:
        return False
    return True


count_perms_memos = {}
def count_perms(parts, broken_pattern, max_space_len, part_index, start_pos):
    # memoize
    if True:
        key = (part_index, start_pos)
        if key in count_perms_memos:
            value = count_perms_memos.get(key)
        else:
            value = _count_perms(parts, broken_pattern, max_space_len, part_index, start_pos)
            count_perms_memos[key] = value
    else:
        value = _count_perms(parts, broken_pattern, max_space_len, part_index, start_pos)

    return value


def _count_perms(parts, broken_pattern, max_space_len, part_index, start_pos):
    part = parts[part_index]
    if not part.is_space:
        if not can_place(part, broken_pattern[start_pos:]):
            return 0
        else:
            new_start_pos = start_pos + part.len
            return count_perms(parts, broken_pattern, max_space_len, part_index + 1, new_start_pos)
    else:
        count = 0
        for i in range(part.min_len, max_space_len+1):
            part.len = i
            if not can_place(part, broken_pattern[start_pos:]):
                if part_index < (len(parts)-1):
                    break
                else:
                    continue
            else:
                if part_index < (len(parts)-1):
                    new_start_pos = start_pos + i
                    count += count_perms(parts, broken_pattern, max_space_len, part_index + 1, new_start_pos)
                else:
                    new_start_pos = start_pos + i
                    if new_start_pos == len(broken_pattern):
                        return 1
                    else:
                        continue
        return count


def part_2(lines):
    total = 0
    for line in lines:
        broken_pattern, criteria = line.split()
        broken_pattern = (broken_pattern + '?') * 4 + broken_pattern
        criteria = (criteria + ',') * 4 + criteria
        parts = create_part_list(criteria)
        global count_perms_memos
        count_perms_memos = {}
        max_space_len = compute_max_space_len(broken_pattern, parts)
        count = count_perms(parts, broken_pattern, max_space_len, 0, 0)
        # print(broken_pattern, criteria, count)
        total += count
    print(total)


with open('day12.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]

part_1(lines)
part_2(lines)