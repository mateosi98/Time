import sys
dir_name = '/Users/mateosallesize/Documents/SRO/Braids/TIME'
sys.path.insert(0, dir_name)

import numpy as np
import pandas as pd
import new_2
import braid_production
import time
import random


from importlib import reload
reload(braid_production)
reload(new_2)

"""""
Creating 10k random braids and counting how many satisfy each condition.

"""

df_size = 10000
strands, length = 3, 12
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

def create_balanced_dataset_new(number_of_braids_of_each_kind, strands = strands, b_len = length):
    braid_half_len = b_len // 2 
    n = strands - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    trivial_braids = []
    non_trivial_braids = []
    c = [0] * 7
    while len(trivial_braids) + len(non_trivial_braids) < df_size:
        braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
        triv, c = new_2.is_trivial(braid, c)
        if triv:
            if not braid in trivial_braids and len(trivial_braids) < number_of_braids_of_each_kind:
                trivial_braids.append(braid)
        else:
            if not braid in non_trivial_braids and len(non_trivial_braids) < number_of_braids_of_each_kind:
                non_trivial_braids.append(braid)
    return c


cs = []
for l in [10,20,30,40,50]:
# for l in [10,12, 14, 16 ,18,20]:
    s = time.time()
    c = create_balanced_dataset_new(df_size, strands,l)
    e = time.time()
    cs.append([l]+c+[e-s])

pd.DataFrame(cs, columns=['Length','CEP', 'CES', 'CEP, CES', 'CES_m', 'CEP, CES_m', 'AUT', 'ces_m == cep_ces', 'time']).to_csv('results_exp_2_large_m.csv', index=False)

# 2.1 = 2264
# 2.2 = 268
# 2.3 = 196
# 2.4 = 160
# sum(np.ones([10*2], dtype=np.int32).reshape(2,10)*(1-3))