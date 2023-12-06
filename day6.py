def count_ways_to_win(times, distances):
    ways_to_win_all = []
    for race in range(len(times)):
        ways_to_win = 0
        race_length = times[race]
        best_distance = distances[race]
        for speed in range(0, race_length):
            time_to_travel = race_length - speed
            distance_traveled = speed * time_to_travel
            if distance_traveled > best_distance:
                ways_to_win += 1
        ways_to_win_all.append(ways_to_win)

    return ways_to_win_all


def multiply_all(nums):
    multiple = 1
    for w in ways_to_win_all:
        multiple *= w
    return multiple


with open('day6.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]

# part 1
times = [int(t.strip()) for t in lines[0].split(':')[1].split()]
distances = [int(t.strip()) for t in lines[1].split(':')[1].split()]
ways_to_win_all = count_ways_to_win(times, distances)
print(f'multiple: {multiply_all(ways_to_win_all)}')

# part 2
times = [int(lines[0].split(':')[1].replace(' ',''))]
distances = [int(lines[1].split(':')[1].replace(' ',''))]
ways_to_win_all = count_ways_to_win(times, distances)
print(f'multiple: {multiply_all(ways_to_win_all)}')