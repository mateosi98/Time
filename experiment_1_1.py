import sys
dir_name = '/Users/mateosallesize/Documents/SRO/Braids/TIME'
sys.path.insert(0, dir_name)

import numpy as np
import pandas as pd
import kitty_lacey
import new_1
import braid_production
import time
import random


from importlib import reload
reload(braid_production)
reload(new_1)
reload(kitty_lacey)

# df_size = 1000
# strands, length = 3, 16
# braid_half_len = length //2

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

def create_balanced_dataset_KL(number_of_braids_of_each_kind, strands, b_len):
    # finish this function to create a dataset for AL
    braid_half_len = b_len // 2 
    n = strands - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    trivial_braids = []
    non_trivial_braids = []
    # while len(trivial_braids) < number_of_braids_of_each_kind or len(non_trivial_braids) < number_of_braids_of_each_kind:
    while len(trivial_braids) + len(non_trivial_braids) < number_of_braids_of_each_kind*2:
        braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
        if kitty_lacey.is_trivial(braid):
            if not braid in trivial_braids and len(trivial_braids) < number_of_braids_of_each_kind:
                trivial_braids.append(braid)
        else:
            if not braid in non_trivial_braids and len(non_trivial_braids) < number_of_braids_of_each_kind:
                non_trivial_braids.append(braid)

def create_balanced_dataset_new(number_of_braids_of_each_kind, strands, b_len):
    # finish this function to create a dataset for AL
    braid_half_len = b_len // 2 
    n = strands - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    trivial_braids = []
    non_trivial_braids = []
    # while len(trivial_braids) < number_of_braids_of_each_kind or len(non_trivial_braids) < number_of_braids_of_each_kind:
    while len(trivial_braids) + len(non_trivial_braids) < number_of_braids_of_each_kind*2:
        braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
        triv = kitty_lacey.is_trivial_June_2023(braid)
        if triv:
            if not braid in trivial_braids and len(trivial_braids) < number_of_braids_of_each_kind:
                trivial_braids.append(braid)
        else:
            if not braid in non_trivial_braids and len(non_trivial_braids) < number_of_braids_of_each_kind:
                non_trivial_braids.append(braid)
    # return trivial_braids, non_trivial_braids 

def timer_create(df, s, l):
    error_count_1, error_count_2 = 0, 0
    s_1 = time.time()
    create_balanced_dataset_KL(df_size,s,l)
    e_1 = time.time()
    s_2 = time.time()
    create_balanced_dataset_new(df_size,strands,length)
    e_2 = time.time()
    # b_all = [i for i in t] + [j for j in nt]
    # for i in t:
    #     if not kitty_lacey.is_trivial(i):
    #         error_count_1 += 1
    # for j in nt:
    #     if kitty_lacey.is_trivial(j):
    #         error_count_2 += 1
    row = [int(df_size*2), length, e_1-s_1, e_2-s_2, error_count_1, error_count_2]
    df.loc[len(df)] = row
    return df

strands, df_size = 3, 1000
lengths = [8,10]
df = pd.DataFrame(columns=['size', 'length', 'time_AUT', 'time_AUT23','e1','e2'])
for length in lengths:
    kitty_lacey.braid_len = length
    df= timer_create(df, strands, length)

df

df.to_csv('results_exp_1_1.csv', index=False)



s1 = time.time()
# kitty_lacey.braid_len = 50
kitty_lacey.is_trivial([-2, 2, 1, 1, -2, 2, -2, -1, -1, -2, -2, -2, 1, 1, 1, 2, -1, 1, 2, 1, -2, 2, -1, -1, -1, -1, 2, 2, -2, -1, -2, -2, 1, 2, 1, -1, -1, -2, 1, 1, 1, -1, 1, 1, 2, 2, -1, -1, -2, 1])
e1 = time.time()
print(e1-s1)
s2 = time.time()
# kitty_lacey.braid_len
# kitty_lacey.braid_half_len
# kitty_lacey.braid_len = 50
# kitty_lacey.braid_half_len = kitty_lacey.braid_len // 2
# kitty_lacey.set_params(3, 50)
kitty_lacey.is_trivial_June_2023([-2, 2, 1, 1, -2, 2, -2, -1, -1, -2, -2, -2, 1, 1, 1, 2, -1, 1, 2, 1, -2, 2, -1, -1, -1, -1, 2, 2, -2, -1, -2, -2, 1, 2, 1, -1, -1, -2, 1, 1, 1, -1, 1, 1, 2, 2, -1, -1, -2, 1])
e2 = time.time()
print(e2-s2)
