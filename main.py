# Beginning Advent of Code. This looks fun.

############## Day 1: Challenge A ##############
"""
f = open('data/day1.data')

make_me_new_data = []
for line in f:
    make_me_new_data.append(int(line))

incrementer = 0
for index_ in range(len(make_me_new_data)):
    if make_me_new_data[index_] > make_me_new_data[index_-1] and index_ > 0:
        incrementer += 1

print(incrementer)

# Answer = 1390
"""

############## Day 1: Challenge B ##############
f = open('data/day1.data')

make_me_new_data = []
for line in f:
    make_me_new_data.append(int(line))

sliding_window_measure = 3
indexes_to_try = len(make_me_new_data) - sliding_window_measure
incrementer = 0
for index_ in range(indexes_to_try):
    a = make_me_new_data[index_] + make_me_new_data[index_+1] + make_me_new_data[index_+2]
    b = make_me_new_data[index_+1] + make_me_new_data[index_+2] + make_me_new_data[index_+3]
    if b > a:
        incrementer += 1

print(incrementer)

# Answer = 1457

