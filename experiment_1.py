import sys
dir_name = '/Users/mateosallesize/Documents/SRO/Braids/TIME'
sys.path.insert(0, dir_name)

import numpy as np
import pandas as pd
import kitty_lacey_for_calling
import new_1
import braid_production
import time
import random


from importlib import reload
reload(braid_production)
reload(new_1)
reload(kitty_lacey_for_calling)

""""
Time comparison between AUT and CEP, CES, AUT creating balanced datasets 
(Using AUT23 in both cases)
"""

df_size = 1000
strands, length = 3, 16
braid_half_len = length //2

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

def create_balanced_dataset_AUT(number_of_braids_of_each_kind, strands = strands, b_len = length):
    # finish this function to create a dataset for AL
    braid_half_len = b_len // 2 
    n = strands - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    trivial_braids = []
    non_trivial_braids = []
    while len(trivial_braids) < number_of_braids_of_each_kind or len(non_trivial_braids) < number_of_braids_of_each_kind:
        # print(len(trivial_braids))
        # generate a random braid
        braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
        # try to add the new braid to the correctly chosen list of braids
        # print(braid)
        if kitty_lacey_for_calling.is_trivial(braid):
            if not braid in trivial_braids and len(trivial_braids) < number_of_braids_of_each_kind:
                trivial_braids.append(braid)
        else:
            if not braid in non_trivial_braids and len(non_trivial_braids) < number_of_braids_of_each_kind:
                non_trivial_braids.append(braid)

def create_balanced_dataset_ALL(number_of_braids_of_each_kind, strands = strands, b_len = length):
    # finish this function to create a dataset for AL
    braid_half_len = b_len // 2 
    n = strands - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    trivial_braids = []
    non_trivial_braids = []
    c = [0] * 4
    while len(trivial_braids) < number_of_braids_of_each_kind or len(non_trivial_braids) < number_of_braids_of_each_kind:
        # print(len(trivial_braids))
        # generate a random braid
        braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
        # try to add the new braid to the correctly chosen list of braids
        # print(braid)
        triv = new_1.is_cep_ces_aut(braid)
        if triv:
            if not braid in trivial_braids and len(trivial_braids) < number_of_braids_of_each_kind:
                trivial_braids.append(braid)
        else:
            if not braid in non_trivial_braids and len(non_trivial_braids) < number_of_braids_of_each_kind:
                non_trivial_braids.append(braid)

def timer_create(df):
    # error_count_1, error_count_2 = 0, 0
    s_1 = time.time()
    create_balanced_dataset_AUT(df_size,strands,length)
    e_1 = time.time()
    s_2 = time.time()
    create_balanced_dataset_ALL(df_size,strands,length)
    e_2 = time.time()
    row = [int(df_size*2), length, e_1-s_1, e_2-s_2]
    df.loc[len(df)] = row
    # print(f'Dataset size: {int(df_size*2)}')
    # print(f'Length: {length}')
    # print(f'K_L: {e_1-s_1}')
    # # print(f'Er_k_l: {error_count_1}')
    # print(f'New: {e_2-s_2}')
    # print(f'Totals: {c}')
    # print(f'Relatives: {per_c}')
    # # print(f'Er_new: {error_count_2}')
    return df

runs = 2
lengths = [10,20,30, 40, 50]
df = pd.DataFrame(columns=['size', 'length', 'time_AUT', 'time_ALL'])
for run in range(runs):
    for length in lengths:
        df = timer_create(df)

df = df.groupby('length').mean()

df.to_csv('results_exp_1_large.csv')


