import random
from itertools import product
import numpy as np
import pandas as pd

# a braid is stretched from left to right
# strand positions are numbered from the bottom to the top
# a positive [negative] crossing is a clockwise [anti-clockwise] half-twist

strands_in_braid = 3
braid_len =10
# braid_len = 10 # note braid_len needs to be even for the birthday paradox code below to work correctly
# braid_half_len = braid_len // 2

# A braid e.g. [-1, 2, 1] is represented as a product of sigma_i,
# with only the index i being recorded in the list;
# a negative index stands for the inverse of a sigma;
# sigma_i takes strand i+1 over strand i.

# an automorphism induced by sigma_i acting on two words x and y
# (which are labels of the two affected strands, that is, strands i and i+1)
# changes them to y and yxy, respectively

def reduce_word_in_kei_group(w):
    reduced = True
    while(reduced):
        reduced = False
        for i in range(len(w)-1):
            if w[i] == w[i+1]:
                w.pop(i)
                w.pop(i)
                reduced = True
                break
    #this function does not return the word, but changes the word as a side effect

def apply_sigma_negative(i, words):
    (words[i], words[i+1]) = (words[i] + words[i+1] + words[i], words[i])
    #this function does not return words, but changes words as a side effect

def apply_sigma_positive(i, words):
    (words[i], words[i+1]) = (words[i+1], words[i+1] + words[i] + words[i+1])
    #this function does not return words, but changes words as a side effect

def braid_to_automorphisms_slow(braid, words):
    for s in braid:
        if s > 0:
            apply_sigma_positive(s-1, words)
        elif s < 0:
            apply_sigma_negative(-s-1, words)
    for i in range(len(words)):
        reduce_word_in_kei_group(words[i])

def braid_to_automorphisms_fast(braid, words):
    if len(braid) <= 1:
        braid_to_automorphisms_slow(braid, words)
    else:
        b1 = braid[:(len(braid)//2)]
        b2 = braid[(len(braid)//2):]
        w1 = [[i] for i in range(1, strands_in_braid+1)]
        #w1 = words
        w2 = [[i] for i in range(1, strands_in_braid+1)]
        braid_to_automorphisms_fast(b1, w1)
        braid_to_automorphisms_fast(b2, w2)
        for i in range(len(words)):
            words[i] = []
            for a in w2[i]:
                #print(w1, w2) 
                words[i].extend(w1[a-1])
    for i in range(len(words)):
        reduce_word_in_kei_group(words[i])
    
def braid_to_automorphisms(braid, words):
    # to choose between different implementations of this function
    braid_to_automorphisms_fast(braid, words)

def inverse_braid(braid):
    return [-a for a in braid[::-1]]

def braids_are_equal(b1, b2):
    w1 = [[i] for i in range(1, strands_in_braid+1)]
    w2 = [[i] for i in range(1, strands_in_braid+1)]
    braid_to_automorphisms(b1, w1)
    braid_to_automorphisms(b2, w2)
    return w1 == w2

def generate_classes_of_equal_braids():
    n = strands_in_braid - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    all_half_braids = list(product(list_of_possible_crossings, repeat=braid_half_len))
    list_of_classes_of_equal_braids = []
    while len(all_half_braids) > 0:
        braid_to_consider = all_half_braids.pop()
        # check if the braid is in one of the classes
        class_found = False
        for i in range(len(list_of_classes_of_equal_braids)):
            if braids_are_equal(braid_to_consider, list_of_classes_of_equal_braids[i][0]):
                class_found = True
                list_of_classes_of_equal_braids[i].append(braid_to_consider)
                break
        if not class_found:
            list_of_classes_of_equal_braids.append([braid_to_consider])
    return list_of_classes_of_equal_braids

def generate_classes_of_equal_braids_with_zeros():
    n = strands_in_braid - 1
    list_of_possible_crossings = list(range(-n, 0)) + [0] + list(range(1, n+1))
    all_half_braids = list(product(list_of_possible_crossings, repeat=braid_half_len))
    list_of_classes_of_equal_braids = []
    while len(all_half_braids) > 0:
        braid_to_consider = all_half_braids.pop()
        # check if the braid is in one of the classes
        class_found = False
        for i in range(len(list_of_classes_of_equal_braids)):
            if braids_are_equal(braid_to_consider, list_of_classes_of_equal_braids[i][0]):
                class_found = True
                list_of_classes_of_equal_braids[i].append(braid_to_consider)
                break
        if not class_found:
            list_of_classes_of_equal_braids.append([braid_to_consider])
    return list_of_classes_of_equal_braids

'''
# testing the 'fast' function
n = strands_in_braid - 1
list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
for braid in list(product(list_of_possible_crossings, repeat=5)):
    ws = [[i] for i in range(1, strands_in_braid+1)]
    braid_to_automorphisms_slow(braid, ws)
    wf = [[i] for i in range(1, strands_in_braid+1)]
    braid_to_automorphisms_fast(braid, wf)
    if not ws == wf:
        print(ws, wf)
'''

def generate_all_trivial_braids(my_strands_in_braid, my_braid_len):
    global strands_in_braid, braid_len, braid_half_len
    strands_in_braid = my_strands_in_braid
    braid_len = my_braid_len
    braid_half_len = braid_len // 2

    list_of_classes_of_equal_braids = generate_classes_of_equal_braids()
    trivial_braids = []
    for c in list_of_classes_of_equal_braids:
        for b1 in c:
            for b2 in c:
                trivial_braids.append(list(b1) + inverse_braid(b2))
    return trivial_braids

#trivial_braids = generate_all_trivial_braids()
#print(trivial_braids)

def is_trivial(braid):
    wf = [[i] for i in range(1, strands_in_braid+1)]
    braid_no_intersections = [[i] for i in range(1, strands_in_braid+1)]
    braid_to_automorphisms_fast(braid, wf)
    return wf == braid_no_intersections

def transform_braid_to_matrix(state, strands, b_len):
    braid_matrix = np.zeros(shape=(strands-1,b_len), dtype=int)
    crossing = 0
    for i in state:
      if i != 0:
        row = abs(i)-1
        number = i/(row+1)
        braid_matrix[row,crossing] = number
      crossing += 1
    return braid_matrix

def create_balanced_dataset(number_of_braids_of_each_kind, strands = strands_in_braid, b_len = braid_len):
    # finish this function to create a dataset for AL
    braid_half_len = b_len // 2 
    n = strands - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    trivial_braids = []
    non_trivial_braids = []
    while len(trivial_braids) < number_of_braids_of_each_kind or len(non_trivial_braids) < number_of_braids_of_each_kind:
        print(len(trivial_braids))
        # generate a random braid
        braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
        # try to add the new braid to the correctly chosen list of braids
        # print(braid)
        if is_trivial(braid):
            if not braid in trivial_braids and len(trivial_braids) < number_of_braids_of_each_kind:
                trivial_braids.append(braid)
        else:
            if not braid in non_trivial_braids and len(non_trivial_braids) < number_of_braids_of_each_kind:
                non_trivial_braids.append(braid)
    
    # Transform to the matrix representation
    trivial_braids = [transform_braid_to_matrix(braid, strands, b_len) for braid in trivial_braids]
    non_trivial_braids = [transform_braid_to_matrix(braid, strands, b_len) for braid in non_trivial_braids]
    trivial_and_not = [1 for i in range(len(trivial_braids))] + [0 for i in range(len(non_trivial_braids))]

    df = pd.DataFrame({}, columns= ['braid','label'])
    df['braid'] = trivial_braids + non_trivial_braids
    df['label'] = trivial_and_not
    df.to_csv(f'trivial-and-not-braids-{b_len}-{strands}-{number_of_braids_of_each_kind}.csv')
    return df

# for strands in [3]:
#     for length in [10]:
#         for size in [2]:
#             strands_in_braid = strands
#             braid_len = length # note braid_len needs to be even for the birthday paradox code below to work correctly
#             braid_half_len = braid_len // 2 
#             create_balanced_dataset(size)

'''
# code counting trivial braids
for braid_half_len in range(1, 10):
    #list_of_classes_of_equal_braids = generate_classes_of_equal_braids()
    list_of_classes_of_equal_braids = generate_classes_of_equal_braids_with_zeros()
    print(2 * braid_half_len, sum([len(c)*len(c) for c in list_of_classes_of_equal_braids]))
'''

'''
# this fragment produces all braids of a given size and states, for each one, if it is trivial
n = strands_in_braid - 1
list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
for braid in list(product(list_of_possible_crossings, repeat=6)):
    wf = [[i] for i in range(1, strands_in_braid+1)]
    braid_no_intersections = [[i] for i in range(1, strands_in_braid+1)]
    braid_to_automorphisms_fast(braid, wf)
    
    if wf == braid_no_intersections: 
        print(braid, wf, braid_no_intersections)
    
    #print(braid, wf == braid_no_intersections)
'''

'''
# this is how the fast function for checking if trivial is used
braid = [1, 2, 1, -2, -1, 2, -1, 1, -2, -2]
print(is_trivial(braid))
'''
