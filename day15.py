import re
import sys


def do_hash(c, value):
    value += ord(c)
    value *= 17
    value %= 256
    return value


def part1(steps):
    total = 0
    for step in steps:
        value = 0
        for c in list(step):
            value = do_hash(c, value)
        total += value
    print(total)


def compute_focusing_power(boxes):
    total = 0
    for box_number, box in enumerate(boxes):
        for slot_number, lens in enumerate(box):
            focusing_power = (box_number+1) * (slot_number+1) * lens.focal_length
            print(f'{lens.label}: {focusing_power}')
            total += focusing_power

    return total


class LabeledLens():
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __eq__(self, other):
        return self.label == other.label

    def __repr__(self):
        return f'{self.label}: {self.focal_length}'


def part2(steps):
    boxes = [[] for box in range(0, 256)]

    for step in steps:
        match = re.search(r'(\w+)([=-])([\d]*)', step)

        label = match.group(1)

        box = 0
        for c in list(label):
            box = do_hash(c, box)

        operation = match.group(2)
        if operation == '-':
            labeled_lens = LabeledLens(label, 0)
            if labeled_lens in boxes[box]:
                boxes[box].remove(labeled_lens)
        elif operation == '=':
            focal_length = match.group(3)
            labeled_lens = LabeledLens(label, int(focal_length))
            if labeled_lens in boxes[box]:
                index = boxes[box].index(labeled_lens)
                boxes[box][index].focal_length = int(focal_length)
            else:
                boxes[box].append(labeled_lens)
        else:
            print("should not happen")
            sys.exit()

    print(compute_focusing_power(boxes))


with open('day15.txt', 'rt') as f:
    steps = f.readline().strip().split(",")

part1(steps)
part2(steps)
