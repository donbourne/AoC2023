import math

map_types = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 'light-to-temperature',
             'temperature-to-humidity', 'humidity-to-location']


def get_location(seed):
    value_to_map = seed
    for map_type in map_types:
        mapping = maps[map_type]
        mapped = False
        for destination, source, length in mapping:
            if not mapped and source <= value_to_map <= (source + length - 1):
                value_to_map = destination + value_to_map - source
                mapped = True
    return value_to_map


def read_input(lines):

    # {'seed-to-soil': [(destination, source, length),(destination, source, length),...]}
    maps = {}
    for map_type in map_types:
        maps.update({map_type: []})

    line_type = 'seeds'
    for line in lines:
        if line == '':
            continue

        if line_type == 'seeds':
            _, seeds = line.split(":")
            seeds = seeds.strip().split()
            seeds = [int(seed) for seed in seeds]
            line_type = None

        elif line.split()[0] in map_types:
            line_type = line.split()[0]

        else:
            destination, source, length = line.split()
            maps[line_type].append((int(destination), int(source), int(length)))

    return seeds, maps


def get_overlap(start_1, length_1, start_2, length_2):
    if start_1 + length_1 - 1 < start_2:
        return None
    if start_2 + length_2 - 1 < start_1:
        return None
    if start_1 <= start_2:
        return max(start_1, start_2), min(start_1 + length_1 - start_2, length_1, length_2)
    if start_1 > start_2:
        return max(start_1, start_2), min(start_2 + length_2 - start_1, length_1, length_2)


def get_matching_blocks(layer, block):
    '''
    returns the list of blocks in specified layer corresponding to the argument block
    '''
    target_source_start = block[1]
    target_source_length = block[2]

    this_layer_blocks = maps[map_types[layer]]
    corresponding_blocks = []
    total_length = 0
    for destination, source, length in this_layer_blocks:
        overlap_block = get_overlap(target_source_start, target_source_length, destination, length)
        if overlap_block:
            # add in the source to the tuple
            overlap_block = (overlap_block[0], overlap_block[0] - destination + source, overlap_block[1])
            corresponding_blocks.append(overlap_block)
            total_length += overlap_block[2]
        if total_length == target_source_length:
            return corresponding_blocks
    corresponding_blocks.append((target_source_start, target_source_start, target_source_length - total_length))
    return corresponding_blocks


def check_seeds(n):
    for seed_range in seeds:
        if seed_range[0] > n:
            continue
        if seed_range[0] + seed_range[1] > n:
            return True
    return False


def go(blocks, layer):
    for block in blocks:
        if layer == 0:
            if check_seeds(block[1]):
                print(f'seed: {block[1]} has lowest location: {get_location(block[1])}')
                return True
        else:
            prev_layer_blocks = get_matching_blocks(layer - 1, block)
            if go(prev_layer_blocks, layer - 1):
                return True
    return False


with open('day5.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]


seeds, maps = read_input(lines)

# part 1
locations = []
for seed in seeds:
    locations.append(get_location(seed))
print(min(locations))

# part 2
new_seeds = []
for i in range(int(len(seeds)/2)):
    new_seeds.append((seeds[i*2], seeds[i*2+1]))
seeds = new_seeds

# brute force - this would take hours to finish
'''
locations = []
counter = 0
min_location = math.inf
for range_start, range_length in seeds:
    for j in range(range_start, range_start+range_length):
        counter += 1
        if counter % 1000000 == 0:
            print(counter)
        location = get_location(j)
        if location < min_location:
            min_location = location
            print(f'min_location = {min_location}')
'''

'''
NEW PLAN...

loop through the blocks of the last layer
for each block create a list of corresponding blocks from the previous layer
recurse until you reach the top then compare to see if any seeds match the block from the first layer

a block is a destination-start / source-start / length tuple
'''

# sort ranges and add explicit ranges wherever there are blanks
for map_type in map_types:
    maps[map_type].sort(key=lambda x: x[0])
    for i in range(len(maps[map_type])):
        if i == 0:
            if maps[map_type][0][0] > 0:
                maps[map_type].insert(0, (0, 0, maps[map_type][0][0]))

        this_range_start = maps[map_type][i][0]
        prev_range_start = maps[map_type][i-1][0]
        prev_range_xend  = maps[map_type][i-1][0] + maps[map_type][i-1][2]
        if this_range_start > prev_range_xend:
            maps[map_type].insert(i, (prev_range_xend, prev_range_xend, this_range_start - prev_range_xend))


layer = len(map_types) - 1
go(maps[map_types[layer]], layer)

print('done')
