'''
heat_map = the input map showing how much heat is lost by entering a space
total_heat_map = map showing amount of heat lost along path from start space up to and including each space

fill(disallowed_moves_list=None):
    fill in bottom right corner with corresponding value from heat map
    create candidate list (list of filled spaces with unfilled adjacent spaces)
    while not done
        sort candidate list by total_heat value
        pop candidate C with the lowest total_heat value
        for each unfilled adjacent space A next to C:
            if space and dir relative to C is not on disallowed_move_list:
                fill in value for A by adding heat map value of A to total_heat value of C
                add A to candidate list

    when filling each space, keep track of:
        total_heat - the total heat value as measured from the start space
        dir_moved - the direction moved from the previous space into this space
        num_dir_moves - the number of consecutive moves in the direction dir_moved after space is filled

    during fill, upon reaching a point where we have hit max moves in direction D:
        choose best of 4 options for what value at end space would be with board filled from scratch with the following restrictions set separately:
            not allowing 4th move in direction D
            not allowing 3rd move in direction D
            not allowing 2nd move in direction D
            not allowing 1st move in direction D
        note that filling rest of the board may result in other situations where the max moves limit is reached, so
        it's necessary to keep a list of disallowed_move_lists. where it is necessary to disallow multiple moves on the
        same board fill, add the permutations to the list:
            [((5,5), UP), ((2,1), UP)]
            [((6,5), UP), ((2,1), UP)]
            [((7,5), UP), ((2,1), UP)]
            [((8,5), UP), ((2,1), UP)]

            [((5,5), UP), ((3,1), UP)]
            [((6,5), UP), ((3,1), UP)]
            [((7,5), UP), ((3,1), UP)]
            [((8,5), UP), ((3,1), UP)]
            ...

        disallowed_move_list = list of (coordinates (R, C), direction D)
            eg. ((5,5), UP) means setting value at (4,5) based on value of (5,5) is not allowed
'''