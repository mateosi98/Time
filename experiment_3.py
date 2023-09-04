import sys
dir_name = '/Users/mateosallesize/Documents/SRO/Braids/TIME'
sys.path.insert(0, dir_name)

import numpy as np
import pandas as pd
import kitty_lacey_for_calling
import new_1
import new_1_c1
import new_3
import braid_production
import time
import random


from importlib import reload
reload(braid_production)
reload(new_1)
reload(new_1_c1)
reload(new_3)


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


def create_balanced_dataset_cep_ces_aut(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
            if len(trivial_braids) < number_of_braids_of_each_kind and not braid in trivial_braids:
                trivial_braids.append(braid)
        else:
            if len(non_trivial_braids) < number_of_braids_of_each_kind and not braid in non_trivial_braids:
                non_trivial_braids.append(braid)

def create_balanced_dataset_cep_aut(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
        triv = new_1_c1.is_cep_aut(braid)
        if triv:
            if len(trivial_braids) < number_of_braids_of_each_kind and not braid in trivial_braids:
                trivial_braids.append(braid)
        else:
            if len(non_trivial_braids) < number_of_braids_of_each_kind and not braid in non_trivial_braids:
                non_trivial_braids.append(braid)

def create_balanced_dataset_ces_cep_aut(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
        triv = new_3.is_ces_cep_aut(braid)
        if triv:
            if len(trivial_braids) < number_of_braids_of_each_kind and not braid in trivial_braids:
                trivial_braids.append(braid)
        else:
            if len(non_trivial_braids) < number_of_braids_of_each_kind and not braid in non_trivial_braids:
                non_trivial_braids.append(braid)

def create_balanced_dataset_aut(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
            if len(trivial_braids) < number_of_braids_of_each_kind and not braid in trivial_braids:
                trivial_braids.append(braid)
        else:
            if len(non_trivial_braids) < number_of_braids_of_each_kind and not braid in non_trivial_braids:
                non_trivial_braids.append(braid)

def create_balanced_dataset_cep_ces_aut_m(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
        if new_1.is_cep_ces_aut_m(braid):
            if len(trivial_braids) < number_of_braids_of_each_kind and not braid in trivial_braids:
                trivial_braids.append(braid)
        else:
            if len(non_trivial_braids) < number_of_braids_of_each_kind and not braid in non_trivial_braids:
                non_trivial_braids.append(braid)

def create_balanced_dataset_ces_aut_m(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
        if new_1.is_ces_aut_m(braid):
            if len(trivial_braids) < number_of_braids_of_each_kind and not braid in trivial_braids:
                trivial_braids.append(braid)
        else:
            if len(non_trivial_braids) < number_of_braids_of_each_kind and not braid in non_trivial_braids:
                non_trivial_braids.append(braid)

def timer_create(df):
    error_count_1, error_count_2 = 0, 0
    s_0 = time.time()
    create_balanced_dataset_cep_ces_aut(df_size,strands,length)
    e_0 = time.time()
    s_1 = time.time()
    create_balanced_dataset_cep_aut(df_size,strands,length)
    e_1 = time.time()
    s_2 = time.time()
    create_balanced_dataset_ces_cep_aut(df_size,strands,length)
    e_2 = time.time()
    s_3 = time.time()
    create_balanced_dataset_aut(df_size,strands,length)
    e_3 = time.time()
    s_5 = time.time()
    create_balanced_dataset_ces_aut_m(df_size,strands,length)
    e_5 = time.time()
    row = [int(df_size*2), length, e_0-s_0, e_1-s_1, e_2-s_2, e_3-s_3,e_5-s_5]
    df.loc[len(df)] = row
    return df


runs = 1
lengths = [10,14,18,22,26,30,34]
df = pd.DataFrame(columns=['size', 'length', 'time_CEP_CES_AUT',
                             'time_CEP_AUT', 'time_CES_CEP_AUT', 
                             'time_AUT',
                             'time_CES_AUT_m'])
for run in range(runs):
    for length in lengths:
        df = timer_create(df)
        print(length)

df = df.groupby('length').mean()
file_name = 'results_exp_3_large_m.csv'
df.to_csv(file_name)

df


###########################################################################################################################################################

import matplotlib.pyplot as plt

exp3 = pd.read_csv('results_exp_3_large_m.csv', index_col=0)
# exp3.loc[34] = df.loc[34]
# exp3.to_csv('results_exp_3_large.csv')
# exp3 = exp3.drop(32)

fig, ax = plt.subplots()
# colors = ['#5DC863', '#21908C', '#440154', '#3B528B', '#FDE725']
colors = ['#5DC863', '#21908C', '#440154', '#3B528B', '#FDE725']
ax.plot(exp3.index, exp3.time_CEP_CES_AUT, marker='o', color=colors[0], label='CEP, CES2, AUT')
ax.plot(exp3.index, exp3.time_CEP_AUT, marker='o', color=colors[1], label='CEP, AUT')
ax.plot(exp3.index, exp3.time_CES_CEP_AUT, marker='o', color=colors[2], label='CES2, CEP, AUT')
ax.plot(exp3.index, exp3.time_CES_AUT_m, marker='o',color=colors[4], label='CES1, AUT')
ax.plot(exp3.index, exp3.time_AUT, marker='o',color=colors[3], label='AUT')
ax.set_xlabel('Length')
ax.set_ylabel('Seconds')
ax.set_yscale('log')
# ax.set_xlim(min(lengths)-1, max(lengths)+1)
ax.set_xticks(exp3.index)
ax.legend(reverse=True) #['AUT','CES, CEP, AUT', 'CEP, AUT', 'CEP, CES, AUT'])
plt.savefig('exp_3_large_log.png')
# plt.show()


fig, ax = plt.subplots()
# colors = ['#5DC863', '#21908C', '#440154', '#3B528B', '#FDE725']
colors = ['#5DC863', '#21908C', '#440154', '#3B528B', '#FDE725']
ax.plot(exp3.index, exp3.time_CEP_CES_AUT, marker='o', color=colors[0], label='CEP, CES2, AUT')
ax.plot(exp3.index, exp3.time_CEP_AUT, marker='o', color=colors[1], label='CEP, AUT')
ax.plot(exp3.index, exp3.time_CES_CEP_AUT, marker='o', color=colors[2], label='CES2, CEP, AUT')
ax.plot(exp3.index, exp3.time_CES_AUT_m, marker='o',color=colors[4], label='CES1, AUT')
ax.plot(exp3.index, exp3.time_AUT, marker='o',color=colors[3], label='AUT')
ax.set_xlabel('Length')
ax.set_ylabel('Seconds')
# ax.set_yscale('log')
# ax.set_xlim(min(lengths)-1, max(lengths)+1)
ax.set_xticks(exp3.index)
ax.legend(reverse=True) #['AUT','CES, CEP, AUT', 'CEP, AUT', 'CEP, CES, AUT'])
plt.savefig('exp_3_large.png')
# plt.show()


fig, ax = plt.subplots()
# colors = ['#5DC863', '#21908C', '#440154', '#3B528B', '#FDE725']
colors = ['#5DC863', '#21908C', '#440154', '#3B528B']
ax.plot(exp3.index, exp3.time_CEP_CES_AUT, marker='o', color=colors[0], label='CEP, CES, AUT')

ax.set_xlabel('Length')
ax.set_ylabel('Seconds')
# ax.set_yscale('log')
# ax.set_xlim(min(lengths)-1, max(lengths)+1)
ax.set_xticks(exp3.index)
ax.legend(reverse=True) #['AUT','CES, CEP, AUT', 'CEP, AUT', 'CEP, CES, AUT'])
# plt.savefig('exp_3_large_log.png')
plt.show()
