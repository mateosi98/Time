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

df_size = 2500
strands, length = 3, 16
braid_half_len = length //2

try:
    df = pd.read_csv(f'trivial-and-not-braids-{length}-{strands}-{df_size}.csv').drop('Unnamed: 0', axis=1)
    df['braid'] = [np.fromstring(braid.replace("[", "").replace("]", "").replace("\n", ""), sep=" ",dtype=int).reshape(1,length*(strands-1)) for braid in df["braid"].values.tolist()]
except:
    df = braid_production.create_balanced_dataset(number_of_braids_of_each_kind=df_size, strands=strands, b_len=length)
    

def to_e0(braid):
    b = np.copy(braid)
    for i in range(b.shape[1]):
        if b[1][i] > 0:
            b[1][i] = b[1][i] + 1
        elif b[1][i] < 0:
            b[1][i] = b[1][i] - 1
    return np.sum(b,axis=0)

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

def timer():
    error_count_1, error_count_2 = 0, 0
    s_1 = time.time()
    for i in range(len(df)):
        braid = np.array(df.loc[i]['braid'])
        label = df.loc[i]['label']
        res = int(kitty_lacey.is_trivial(to_e0(braid)))
        if res != label:
            error_count_1 +=1
    e_1 = time.time()
    s_2 = time.time()
    for j in range(len(df)):
        braid = np.array(df.loc[j]['braid'])
        label = df.loc[j]['label']
        res = int(not new_1.is_trivial(to_e0(braid)))
        if res != label:
            error_count_2 += 1 
    e_2 = time.time()
    print(f'Dataset size: {len(df)}')
    print(f'Length: {length}')
    print(f'K_L: {e_1-s_1}')
    # print(f'Er_k_l: {error_count_1}')
    print(f'New: {e_2-s_2}')
    # print(f'Er_new: {error_count_2}')

# timer()

def create_balanced_dataset_KL(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
        if kitty_lacey.is_trivial(braid):
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

def create_balanced_dataset_new(number_of_braids_of_each_kind, strands = strands, b_len = length):
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
        triv, c = new_1.is_trivial(braid)
        if triv:
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

def timer_create(df):
    error_count_1, error_count_2 = 0, 0
    s_1 = time.time()
    create_balanced_dataset_KL(df_size,strands,length)
    e_1 = time.time()
    s_2 = time.time()
    create_balanced_dataset_new(df_size,strands,length)
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

lengths = [10,12,14,16,18,20]
df = pd.DataFrame(columns=['size', 'length', 'time_kl', 'time_new',
                            'total_c1','total_c2', 'total_c3', 'total_c4',
                            '%_c1', '%_c2', '%_c3', '%_c4'])
for length in lengths:
    df = timer_create(df)

df.to_csv('timer_KL_vs_new.csv', index=False)


import matplotlib.pyplot as plt

exp3 = pd.read_csv('timer_exp_3.csv', index_col=0)
exp3.columns
num_cols = ['time_c1', 'time_c1_no_c2', 'time_c2', 'time_KL']
for col in num_cols:
    exp3[col+'_log'] = np.log(exp3[col])
exp3

fig, ax = plt.subplots()
colors = ['#5DC863', '#21908C', '#440154', '#3B528B', '#FDE725']
colors = ['#5DC863', '#21908C', '#440154', '#3B528B']
ax.plot(exp3.length, exp3.time_c1, marker='o', color=colors[0])
ax.plot(exp3.length, exp3.time_c1_no_c2, marker='o', color=colors[1])
ax.plot(exp3.length, exp3.time_c2, marker='o', color=colors[2])
ax.plot(exp3.length, exp3.time_KL, marker='o',color=colors[3])
ax.set_xlabel('Length')
ax.set_ylabel('Seconds')
ax.set_yscale('log')
ax.legend(['CEP, CES, AUT', 'CEP, AUT', 'CES, CEP, AUT', 'AUT'])
plt.show()