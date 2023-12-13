import numpy as np

def go(patterns_nd, tolerance):
    total = 0
    for pattern in patterns_nd:
        for row in range(0, (pattern.shape[0] - 1)):
            if np.sum(pattern[row, :] != pattern[row+1, :]) <= tolerance:
                flipud_pattern = np.flipud(pattern)
                pattern_1 = flipud_pattern[-(row + 1):]
                pattern_2 = pattern[row + 1:]
                overlap = min(pattern_1.shape[0], pattern_2.shape[0])
                if np.sum(pattern_1[0:overlap] != pattern_2[0:overlap]) == tolerance:
                    # print(f"row flip {row+1}")
                    total += 100*(row+1)

        for col in range(0, (pattern.shape[1] - 1)):
            if np.sum(pattern[:, col] != pattern[:, col+1]) <= tolerance:
                fliplr_pattern = np.fliplr(pattern)
                pattern_1 = fliplr_pattern[:, -(col + 1):]
                pattern_2 = pattern[:, col + 1:]
                overlap = min(pattern_1.shape[1], pattern_2.shape[1])
                if np.sum(pattern_1[:, 0:overlap] != pattern_2[:, 0:overlap]) == tolerance:
                    # print(f"col flip {col+1}")
                    total += col+1
    print(total)


with open('day13.txt', 'rt') as f:
    lines = [list(line.strip()) for line in f.readlines()]

patterns_nd = []
pattern = []
for line in lines:
    if len(line) == 0:
        patterns_nd.append(np.array(pattern, dtype=str))
        pattern = []
    else:
        pattern.append(line)
patterns_nd.append(np.array(pattern, dtype=str))

go(patterns_nd, 0)
go(patterns_nd, 1)
