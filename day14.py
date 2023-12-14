import numpy as np
import re

with open('day14.txt', 'rt') as f:
    lines = [list(line.strip()) for line in f.readlines()]

arr = np.array(lines)
# print(arr)
arr_rotated = np.rot90(arr)
# print(arr_rotated)
lines_rotated = arr_rotated.tolist()
strs_rotated = [''.join(line) for line in lines_rotated]
print(lines_rotated)
strs_rolled = []
for s in strs_rotated:
    done = False
    while not done:
        new_s = re.sub(r'(\.+)O', r'O\1', s)
        print(f'{s}\n{new_s}\n')
        if s == new_s:
            done = True
            strs_rolled.append(new_s)
        else:
            s = new_s

print(strs_rolled)
arr = np.array([list(s) for s in strs_rolled])
print(arr)
multipliers = np.arange(arr.shape[1], 0, -1)
print(multipliers)
count = np.sum(arr == 'O', axis=0)
print(count)
score = count * multipliers
print(score)
score = np.sum(score)
print(score)
