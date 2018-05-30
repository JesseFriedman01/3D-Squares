import itertools
from multiprocessing import Pool

#####################################################################
# def piece_match(position_num)
# Purpose: as an input, it takes the position number on the piece under
# observation as an input and returns the other pieces and location of
# the body part that the position number of the input corresponds to
# Pre-conditions: position_num is between 0 and 3
# Post-conditions: none
######################################################################

def piece_match(position_num):

    if position_num == 0:
        match_list = [[3, 0], [4, 1], [5, 2], [6, 3], [7, 4], [8, 5]]  # if looking for a match for position 0 (top), piece 3 & 0 must go together, etc.
        pos_of_matching_piece = 2                                      # with a body part in position 0, the matching body part is in position 2 on the other piece

    elif position_num == 1:
        match_list = [[0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [7, 8]]
        pos_of_matching_piece = 3

    elif position_num == 2:
        match_list = [[0, 3], [1, 4], [2, 5], [3, 6], [4, 7], [5, 8]]
        pos_of_matching_piece = 0

    elif position_num == 3:
        match_list = [[1, 0], [2, 1], [4, 3], [5, 4], [7, 6], [8, 7]]
        pos_of_matching_piece = 1

    return match_list, pos_of_matching_piece


#######################################################################
# def spin_pieces(puzzle_pieces)
# Purpose: as an input, it takes a shuffled puzzle_pieces_initial
# (see main) and iterates through all of the combinations of this list
# sending one iteration at a time to match_count
# Pre-conditions: puzzle_pieces is a list that has 9 sub-lists
# representing each piece and its 4 body part IDs (1 - 8).
# Post-conditions: none
#######################################################################

def spin_pieces(puzzle_pieces):

    spin_combos = list(itertools.product([0, 1, 2, 3], repeat=9)) # produces a template of all of the combinations of 4 rotations on 9 different pieces

    perm_list = []

    for num_combos in range(len(spin_combos)):                    # produces a list of 4 rotations on different pieces using the template produced by spin_combos
        counter = 0
        perm_list_temp = []
        for j in spin_combos[num_combos]:
            perm_list_temp.append(puzzle_pieces[counter][j])

            if counter == 8:
                break
            counter += 1

            perm_list.append(perm_list_temp)


    match_count(perm_list) # call match_count with the created

#####################################################################
# def match_count(perm_list)
# Purpose: takes a given configuration of pieces on the board as an input
# and logs the number of matches
# Pre-conditions: perm_list is a list of all of the combinations of
# rotations for a given layout
# Post-conditions: none
######################################################################

def match_count(perm_list):

    match_counter=0
    counter=0

    for sets in range (len(perm_list)):
        counter+=1
        if match_counter >= 18:                                                  # counts each match twice. So this is logging each configuration with at least 9 matches on the board

            text_file = open("results.txt", "w")                                 # write the number of matches and the configuration of pieces (the layout) to a file

            text_file.write(str(match_counter) + " " + str(perm_list[sets]))
            text_file.close()

            print('Match counter:', match_counter)                               # also output it to command line
            print(perm_list[sets])

        match_counter = 0

        for side_of_piece in range(4):
            match_list, pos_of_matching_piece = piece_match(side_of_piece)
            for j in range(len(match_list)):
                value_in_piece_A = (perm_list[sets][match_list[j][0]][side_of_piece])             # assigns the ID of the body part of the piece under observation
                value_in_piece_B = (perm_list[sets][match_list[j][1]][pos_of_matching_piece])     # assigns the ID of the body part of the piece being compared to, based on its location
                if abs(value_in_piece_A - value_in_piece_B) != 4:                                 # if the difference isn't equal to 4, break the loop and move into next board layout
                    break
                if abs(value_in_piece_A-value_in_piece_B) == 4:                                   # if the difference is 4, the pieces match and increment match_counter
                    match_counter=match_counter+1


#####################################################################
# MAIN
#####################################################################

location_combos = list(itertools.permutations([0,1,2,3,4,5,6,7,8]))             # produces a template of all of the permutations of 9 different values (0 - 8)

puzzle_pieces_initial =  [                                                      # sets an initial layout of the pieces on the board. Each piece has 4 values representing the ID of the body part in a particular direction
                 [ [5,8,2,3], [3,5,8,2], [2,3,5,8], [8,2,3,5] ],#0              # here piece 0 has an initial value of 5, 8, 2, 3. Thus it has a purple tail in position 0 (top), yellow/orange tail in position 1 (right), etc. It is than "rotated 3 times".
                 [ [2,1,3,7], [7,2,1,3], [3,7,2,1], [1,3,7,2] ],#1
                 [ [8,7,6,5], [5,8,7,6], [6,5,8,7], [7,6,5,8] ],#2
                 [ [6,7,1,4], [4,6,7,1], [1,4,6,7], [7,1,4,6] ],#3
                 [ [6,4,1,7], [7,6,4,1], [1,7,6,4], [4,1,7,6] ],#4
                 [ [5,3,2,4], [4,5,3,2], [2,4,5,3], [3,2,4,5] ],#5
                 [ [6,3,4,8], [8,6,3,4], [4,8,6,3], [3,4,8,6] ],#6
                 [ [1,6,5,4], [4,1,6,5], [5,4,1,6], [6,5,4,1] ],#7
                 [ [1,3,6,4], [4,1,3,6], [6,4,1,3], [3,6,4,1] ],#8
                 ]

perm_list_temp=[]
perm_list=[]

for a in range(len(location_combos)):                                           # produces a list of all of the combinations of layouts with a given piece's rotational configuration AND placement on the board. So each element in the list is puzzle_pieces_initial, shuffled.
    counter=0
    perm_list_temp = []
    for j in location_combos[a]:
        perm_list_temp.append(puzzle_pieces_initial[j])

        perm_list.append(perm_list_temp)

if __name__ == '__main__':
    p = Pool(processes=15)                                                      # use multiprocessing to maximize CPU allocation and reduce overall runtime (hopefully without crashing computer). 15 may be too high/low depending on the computer.
    data = p.map(spin_pieces, [perm_list[i] for i in range(len(perm_list))]  )
    p.close()

