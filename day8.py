import math
import re

with open('day8.txt') as f:
    lines = [line.strip() for line in f.readlines()]

instructions = list(lines[0])
instructions = [0 if i == 'L' else 1 for i in instructions]
node_map = {}
for line in lines[2:]:
    node, next = line.split('=')
    node = node.strip()
    next = re.sub('[\(\)]', '', next)
    next = [n.strip() for n in next.split(',')]
    node_map[node] = next


def steps_to_x(x, current_node):
    num_steps = 0
    at_x = False
    while not at_x:
        instruction = instructions[num_steps % len(instructions)]
        current_node = node_map[current_node][instruction]
        num_steps += 1
        if x(current_node):
            at_x = True

    return num_steps


def part_2():
    current_nodes = [node for node in node_map.keys() if node[2] == 'A']
    steps_to_z = []
    for node in current_nodes:
        steps_to_z.append(steps_to_x(lambda x: x[2] == 'Z', node))
        steps_to_z = [int(x) for x in steps_to_z]
    return math.lcm(*steps_to_z)


print(steps_to_x(lambda x: x == 'ZZZ', 'AAA'))
print(part_2())