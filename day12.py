'''
start with the sequence of numbers
create a string representing valid permutations
    eg. 3,2,1 in a total size of 12
    {} = spaces
    [] = blocks (#s)
    numbers inside brackets represent how long that group is
    { 0+ }[ 3 ]{ 1+ }[ 2 ]{ 1+ }[ 1 ]{ 0+ }  min_needed: 3+1+2+1+1=8  max_space: 12-8=4  max_block_len: 3  min_block_len: 1
look at the map to add constraints to groups
    ?###????????
    { min:0 max:1 }[ min:3 max:max_block_len ]{ min:0 max:(12-3)=9 }
    block has min/max len of 3.  since it's "done", check if there is unique item in list matching len of 3
        first item in list is 3... adjust all spaces before it accordingly
        { fixed 1 }[ fixed 3 ]{ min:0 max:(12-3)=9 }  2,1
            add to valid permutations: { min:0 max:(12-3)=9 }  2,1

'''