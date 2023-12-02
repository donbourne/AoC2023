def strip_elements(s):
    return [x.strip() for x in s]


with (open('day2.txt', 'rt') as f):
    lines = f.readlines()

total_1 = total_2 = 0
max_cubes_available = {'red': 12, 'green': 13, 'blue': 14}
for game_num, line in enumerate(lines):
    line = line.strip()
    game_rounds = strip_elements(line.split(':')[1].split(';'))
    impossible = False
    min_cubes_needed = {'red': 0, 'green': 0, 'blue': 0}
    for game_round in game_rounds:
        cubes_used_colors = strip_elements(game_round.split(','))
        for cubes_used in cubes_used_colors:
            cubes_used_num, cubes_used_color = cubes_used.split(' ')
            cubes_used_num = int(cubes_used_num)
            if max_cubes_available[cubes_used_color] < cubes_used_num:
                impossible = True
            if min_cubes_needed[cubes_used_color] < cubes_used_num:
                min_cubes_needed[cubes_used_color] = cubes_used_num
    if not impossible:
        total_1 += game_num + 1
    power = 1
    for value in min_cubes_needed.values():
        power *= value
    total_2 += power

print(total_1, total_2)