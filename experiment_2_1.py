import sys
dir_name = '/Users/mateosallesize/Documents/SRO/Braids/TIME'
sys.path.insert(0, dir_name)

import numpy as np
import pandas as pd
import kitty_lacey
import new_2_1
import braid_production
import time
import random


from importlib import reload
reload(braid_production)
reload(new_2_1)

""""
Create 10,000 random braids and check which ones satisfy each condition.
Take the times to satisfy each condition.
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

def create_dataset(number_of_braids, strands = strands, b_len = length):
    n = strands - 1
    list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    random_braids = []
    # c, t, t_aut, t_aut_max = [0] * 3, [0] * 4, [], 0
    while len(random_braids) < number_of_braids:
        # generate a random braid
        braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
        random_braids.append(braid)
    return random_braids

a = [[1, 2], [2, 3], [3, 4]]
b = [[1, 2], [2, 3]]
[value for value in a if value in b]

def check_conditions(dataset):
    c, t, t_aut, t_aut_max = [0] * 4, [0] * 5, [], 0
    list_cep, list_ces, list_ces_m, list_triv = [], [], [],[]
    for braid in dataset:
        cep, c, t = new_2_1.is_cep(braid, c, t)
        if cep:
            list_cep.append(braid)
    for braid in list_cep:
        ces, c, t = new_2_1.is_ces(braid, c, t)
        if ces:
            list_ces.append(braid)
    for braid in list_cep:
        ces_m, c, t = new_2_1.is_ces_m(braid, c, t)
        if ces_m:
            list_ces_m.append(braid)
    if list_ces_m == [value for value in list_cep if value in list_ces]:
        ces_m_equal_cep_ces = True
    else:
        ces_m_equal_cep_ces = False
    for braid in list_ces:
        triv, c, t = new_2_1.is_aut(braid, c, t)
        t_aut.append(t[4])
        if triv:
            list_triv.append(braid)
        if t[4] >= t_aut_max:
            b_max = braid.copy()
            t_aut_max = max(t_aut)
    return c, t, b_max, t_aut_max, ces_m_equal_cep_ces


cs = []
for run in range(10):
    for l in [10,20,30,40,50]:
        data = create_dataset(df_size, strands, l)
        s = time.time()
        c, t, b_max, t_max, cm_e_cc = check_conditions(data)
        e = time.time()
        cs.append([run+1,l]+c+t[:4]+[b_max]+[t_max]+[cm_e_cc])
        print(f"{str(run+1)}.{str(l)}")


results = pd.DataFrame(cs, columns=['Run','Length','CEP', 'CES', 'CES_m', 'AUT', 'CEP_t', 'CES_t', 'CES_t_m', 'AUT_t', 'Braid_max', 'Time_max', 'CES_m == CEP,CES'])

results['T_t'] = results.CEP_t + results.CES_t + results.AUT_t 

results

mean_results = results[['Length','CEP', 'CES', 'CES_m', 'AUT', 'CEP_t', 'CES_t', 'CES_t_m', 'AUT_t', 'T_t']].groupby('Length').mean()

mean_results

b_max = results[(results.Time_max == results.Time_max.max())]['Braid_max'].values.tolist()[0]
b_max

# results.to_csv('results_exp_2_1_.csv', index=False)
mean_results.to_csv('results_exp_2_1_large.csv')

# 2.1 = 2264
# 2.2 = 268
# 2.3 = 196
# 2.4 = 160
# sum(np.ones([10*2], dtype=np.int32).reshape(2,10)*(1-3))


# def create_dataset_full(number_of_braids, strands = strands, b_len = length):
#     # finish this function to create a dataset for AL
#     braid_half_len = b_len // 2 
#     n = strands - 1
#     list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
#     random_braids = []
#     c, t, t_aut, t_aut_max = [0] * 3, [0] * 4, [], 0
#     # while len(trivial_braids) < number_of_braids_of_each_kind or len(non_trivial_braids) < number_of_braids_of_each_kind:
#     while len(random_braids) < number_of_braids:
#         # generate a random braid
#         braid = [random.choice(list_of_possible_crossings) for _ in range(b_len)]
#         triv, c, t = new_2_1.is_trivial(braid, c, t)
#         t_aut.append(t[3])
#         random_braids.append(braid)
#         if t[3] >= t_aut_max:
#             b_max = braid.copy()
#             t_aut_max = max(t_aut)
#     return c, t, b_max, t_aut_max