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

def pattern_to_re(pattern):


def check_valid(pattern, criteria):
    pattern = pattern_to_re(pattern)




def generate_and_check_patterns(broken_pattern, criteria):
    # count number of question marks
    num_question_marks = 0
    for c in broken_pattern:
        if c == '?':
            num_question_marks += 1

    # generate binary numbers that will be used to represent # or .
    valid_count = 0
    for i in range(0, int(math.pow(2,num_question_marks))):
        bin_i = f'{i:b}'.rjust(num_question_marks,'0')
        s = ''
        bin_i_index = 0
        for c in broken_pattern:
            if c == '?':
                s += char_map[bin_i[bin_i_index]]
                bin_i_index += 1
            else:
                s += c
        print(s)
        if check_valid(s, criteria):
            valid_count += 1

    return valid_count



with open('day12-p1.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]
print(lines)

total = 0
for line in lines:
    broken_pattern, criteria = line.split()
    print(broken_pattern, criteria)
    total += generate_and_check_patterns(broken_pattern, criteria)
print(total)




'''
start with the sequence of numbers
create an object representation of valid permutations
    eg. 3,2,1 in a total size of 12
    {} = spaces
    [] = blocks (#s)
    numbers inside brackets represent how long that group is
    { 0+ }[ 3 ]{ 1+ }[ 2 ]{ 1+ }[ 1 ]{ 0+ }  min_needed: 3+1+2+1+1=8  max_space: 12-8=4  max_block_len: 3  min_block_len: 1
look at the map to add constraints to groups
    ?###????????
    { min:0 max:1 }[ min:3 max:max_block_len ]{ min:0 max:(12-3)=9 }
    block has min/max len of 3.  since it's "done", check if there is unique item in list matching len of 3
        first item in list is 3... adjust all spaces before it accordingly
        { fixed 1 }[ fixed 3 ]{ min:0 max:(12-3)=9 }  2,1
            add to valid permutations: { min:0 max:(12-3)=9 }  2,1

  valid permutations ('?###????????', '3,2,1')
= valid permutations ('????????', '2,1')



'''