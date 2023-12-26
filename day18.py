import numpy as np
from nd_util import pretty_print

# part 1
def connect_points(arr, p1, p2, row_offset, col_offset):
    r1, c1 = p1
    r2, c2 = p2
    lower_r, upper_r = min(r1, r2), max(r1, r2)
    lower_c, upper_c = min(c1, c2), max(c1, c2)
    for r in range(lower_r, upper_r + 1):
        for c in range(lower_c, upper_c+1):
            arr[(r-row_offset, c-col_offset)] = '#'


def fill(arr):
    explore = [(0, 0)]
    while explore:
        point = explore.pop()
        if (arr.shape[0]-1) >= point[0] >= 0 and (arr.shape[1]-1) >= point[1] >= 0:
            if arr[point] == '.' or arr[point] == '0':
                arr[point] = 'O'
                explore.extend([(point[0], point[1]-1), (point[0], point[1]+1), (point[0]-1, point[1]), (point[0]+1, point[1])])


def directions_to_points(directions, distances):
    # convert inputs into a list of point coordinates
    points = []
    row = 0
    col = 0
    points.append((row, col))
    for direction, distance in zip(directions, distances):
        if direction == 'R':
            col += distance
        elif direction == 'L':
            col -= distance
        elif direction == 'U':
            row -= distance
        elif direction == 'D':
            row += distance
        else:
            print(f'invalid direction: {direction}')
        points.append((row, col))
    return points


with open('day18.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]

directions = []
distances = []
colors = []

for line in lines:
    direction, distance, color = line.strip().split()
    directions.append(direction)
    distances.append(int(distance))
    colors.append(color)

points = directions_to_points(directions, distances)

# draw the map
rows = np.array([row for row, col in points])
cols = np.array([col for row, col in points])

max_row = max(rows)
max_col = max(cols)
min_row = min(rows)
min_col = min(cols)

height = max_row - min_row
width = max_col - min_col

row_offset = min_row
col_offset = min_col

arr = np.zeros((height+1, width+1), dtype=str)
arr[:, :] = '.'

arr[rows-row_offset, cols-col_offset] = '#'

# connect the points
for i in range(len(points)-1):
    connect_points(arr, points[i], points[i+1], row_offset, col_offset)

# pad the array by 1 and fill the outside
arr = np.pad(arr,1)
fill(arr)

# unpad
arr = arr[1:-1, 1:-1]
# pretty_print(arr)

# count
inside_count = arr.shape[0] * arr.shape[1] - np.sum(arr == 'O')
print(inside_count)

# part 2
# shoelace algorithm from https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem
def inside_area(points):
    value1 = value2 = 0
    for i in range(len(points)):
        if i == len(points)-1:
            value1 += points[i][0] * points[0][1]
            value2 += points[i][1] * points[0][0]
        else:
            value1 += points[i][0] * points[i+1][1]
            value2 += points[i][1] * points[i+1][0]
    return 0.5 * abs(value1 - value2)


def calculate_perimeter(points):
    perimeter = 0
    for i in range(len(points)):
        if i == len(points)-1:
            perimeter += abs(points[i][0] - points[0][0]) + abs(points[i][1] - points[0][1])
        else:
            perimeter += abs(points[i][0]-points[i+1][0]) + abs(points[i][1]-points[i+1][1])
    return perimeter


distances = []
directions = []
for color in colors:
    distances.append(int(color[2:7], 16))
    directions.append(color[7])

directions_to_letters = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}
directions = [directions_to_letters[direction] for direction in directions]
points = directions_to_points(directions, distances)

# calculate area using shoelace algorithm (assumes points are in middle of squares)
area = inside_area(points)

# shoelace algorithm calculates areas between points
# day18 puzzle wants areas of squares centered at points plus the area inside the squares
# to get from A(sa) to A(day18)...
# A(day18) = A(sa) + 0.5*vert + 0.5*horiz + 0.25*inside_corners -0.25*outside_corners
# because this is a loop with 90 degree turns, there will be 4 more inside corners than outside corners, so
# A(day18) = A(sa) + 0.5*vert + 0.5*horiz + 1
# and vert + horiz = perimeter, so
# A(day18) = A(sa) + 0.5*perimeter + 1

perimeter = calculate_perimeter(points)

print(area + 0.5*perimeter + 1)