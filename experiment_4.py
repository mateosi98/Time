import sys
dir_name = '/Users/mateosallesize/Documents/SRO/Braids/TIME'
sys.path.insert(0, dir_name)

import numpy as np
import pandas as pd
import kitty_lacey
import new_4
import braid_production
import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns


from importlib import reload
reload(braid_production)
reload(new_4)

""""
Create 10,000 random braids and take the times to check AUT
Then take the times to check CEP, CES, AUT
Bar plot
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

def check_conditions(dataset):
    c, t, t_aut, t_all = [0] * 3, [0] * 3, [], []
    # list_cep, list_ces, list_triv = [], [], []
    for braid in dataset:
        triv, c, t = new_4.is_aut(braid, c, t)
        t_aut.append(t[2])
    for braid in dataset:
        cep, c, t = new_4.is_cep(braid, c, t)
        if cep:
            ces, c, t = new_4.is_ces(braid, c, t)
            if ces:
                triv, c, t = new_4.is_aut(braid, c, t)
                t_all.append(sum(t))
            else:
                t_all.append(sum(t[:2]))
        else:
            t_all.append(t[0])
    return np.array(t_aut), np.array(t_all)


cs = []
for run in range(1):
    for l in [20]:
        data = create_dataset(df_size, strands, l)
        s = time.time()
        t_aut, t_cca = check_conditions(data)
        e = time.time()
        print(f"{str(run+1)}.{str(l)}")



# FULL HIST
t_all = [a for a in t_aut] + [b for b in t_cca]
bin_edges = np.logspace(np.log10(min(t_all)), np.log10(max(t_all)), 50)
plt.hist(t_aut, bins=bin_edges, color = '#5DC863', label = 'AUT')
plt.hist(t_cca, bins=bin_edges, color = '#3B528B', label = 'CEP, CES, AUT')
plt.xscale("log")
plt.xlabel('Seconds')
plt.ylabel('Number of braids')
plt.legend()
plt.savefig('exp_4_hist.png')
plt.show()


# ZOOM HIST 
bin_edges = np.logspace(np.log10(min(t_aut)), np.log10(max(t_aut)), 50)
plt.hist(t_aut, bins=bin_edges, color = '#5DC863', label = 'AUT')
plt.hist(t_cca, bins=bin_edges, color = '#3B528B', label = 'CEP, CES, AUT')
plt.xscale("log")
plt.xlabel('Seconds')
plt.ylabel('Number of braids')
plt.legend()
plt.savefig('exp_4_hist_zoom.png')
plt.show()




# data = {'AUT': t_aut, 'CEP, CES, AUT': t_cca}
# df = pd.DataFrame(data)
# sns.kdeplot(data=df)
# plt.yscale('log')
# plt.title('Kernel Density Estimation Plot')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Density')
# plt.show()



# bin_limits = [np.linspace(min(data[:, 0]), max(data[:, 0]), 11),
#                 np.linspace(min(data[:, 1]), max(data[:, 1]), 11)]
# plt.hist2d(data[:,0], data[:,1], bins = bin_limits)
# plt.hist(data[:,0], bins = 'auto')
# plt.hist(data[:,1], bins = 'auto')
# # plt.colorbar()
# plt.show()


# x = range(len(t_aut))
# data = np.column_stack((t_aut,t_all))
# plt.plot(x, t_aut, label='AUT')
# plt.plot(x, t_all, label='CEP, CES, AUT')
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.legend()
# plt.show()



# results = pd.DataFrame(cs, columns=['Run','Length','CEP', 'CES', 'AUT', 'CEP_t', 'CES_t', 'AUT_t', 'Braid_max', 'Time_max'])
# results['T_t'] = results.CEP_t + results.CES_t + results.AUT_t 

# results

# mean_results = results[['Length','CEP', 'CES', 'AUT', 'CEP_t', 'CES_t', 'AUT_t', 'T_t']].groupby('Length').mean()

# mean_results

# b_max = results[(results.Time_max == results.Time_max.max())]['Braid_max'].values.tolist()[0]
# b_max

# results.to_csv('results_exp_2_1_large.csv', index=False)
# mean_results.to_csv('mean_results_exp_2_1_large.csv')


# 2.1 = 2264
# 2.2 = 268
# 2.3 = 196
# 2.4 = 160
# sum(np.ones([10*2], dtype=np.int32).reshape(2,10)*(1-3))
# t_all = [a for a in t_aut] + [b for b in t_cca]
# # bin_edges = np.logspace(np.log10(0.000001), np.log10(max(t_all)), 50)
# fig, ax = plt.subplots()
# bin_edges = np.logspace(np.log10(min(t_all)), np.log10(max(t_all)), 50)
# plt.hist(t_aut, bins=bin_edges, color = '#5DC863', label = 'AUT')
# plt.hist(t_cca, bins=bin_edges, color = '#3B528B', label = 'CEP, CES, AUT')
# abs(np.log10(max(t_aut)-min(t_aut)))
# rect = patches.Rectangle((np.log10(min(t_aut)), 0), abs(np.log10(max(t_aut)-min(t_aut))), 2000,
#                          linewidth=1, edgecolor='r', facecolor='none', transform = plt.gca().transAxes)
# plt.gca().add_patch(rect)
# plt.xscale("log")
# plt.xlabel('Seconds')
# plt.ylabel('Number of braids')
# plt.legend()
# # plt.savefig('exp_4_hist.png')
# plt.show()

