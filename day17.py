'''
heat_map = the input map showing how much heat is lost by entering a space
tot_heat_map[0..2, dir] = the min possible total heat loss from each space to the finish for case where you have
                  0..2 straight moves allowed after entering that space and have last moved in direction dir


populate tot_heat_map[0] value is min(tot_heat_map[2] for adjacent spaces not in reverse nor dir directions)
populate tot_heat_map[1] value is min(tot_heat_map[2] for adjacent spaces not in reverse nor dir directions, tot_heat_map[0] for space in dir direction)
populate tot_heat_map[2] value is min(tot_heat_map[2] for adjacent spaces not in reverse nor dir directions, tot_heat_map[1] for space in dir direction)


fill:
    fill in bottom right corner with corresponding value from heat map
    create candidate list (list of filled spaces with unfilled adjacent spaces)
    while not done
        sort candidate list by value
        pop candidate with the lowest value
        fill in values for spaces adjacent to candidate by adding heat map value of each adjacent space to candidate value
        add newly filled spaces to candidate list

fill (0, right):
    fill in bottom right corner with corresponding value from heat map
    create candidate list (list of filled spaces with unfilled adjacent spaces)
    while not done
        sort candidate list by value
        pop candidate with the lowest value
        fill in values for ABOVE/BELOW spaces that are adjacent to candidate by adding heat map value of each adjacent space to candidate value
        add newly filled spaces to candidate list



0, right -

instead of adjacent...
next valid
    0, increasing col - increase / decrease row
    0, decreasing col - increase / decrease row
    0, increasing row - increase / decrease col
    0, decreasing row - increase / decrease col


0R = min(3U, 3D)

3U = min(2U, 3L, 3R)
2U = min(1U, 3L, 3R)
1U = min(0U, 3L, 3R)
0U = min(3L, 3R)



'''