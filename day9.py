import numpy as np


def create_diffs(sequence):
    diffs = []
    diff = np.array(sequence)
    diffs.append(diff)
    while diff.any().sum() != 0:
        diff = np.diff(diff)
        diffs.append(diff)
    return diffs


def extrapolate(diff_group, forwards):
    append = lambda x, y: np.append(x, y)
    prepend = lambda x, y: np.insert(x, 0, y)
    add = append if forwards else prepend

    diff_group[-1] = add(diff_group[-1], 0)
    for i in range(len(diff_group)-2, -1, -1):
        if forwards:
            diff_group[i] = add(diff_group[i], diff_group[i][-1] + diff_group[i + 1][-1])
        else:
            diff_group[i] = add(diff_group[i], diff_group[i][0] - diff_group[i + 1][0])


with open('day9.txt') as f:
    lines = [line.strip() for line in f.readlines()]
sequences = [line.split() for line in lines]
sequences = [np.array(sequence).astype(int).tolist() for sequence in sequences]

for forwards in [True, False]:
    total = 0
    for sequence in sequences:
        diff_group = create_diffs(sequence)
        extrapolate(diff_group, forwards)
        index = -1 if forwards else 0
        total += diff_group[0][index]

    print(total)