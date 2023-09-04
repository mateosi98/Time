import itertools
from random import shuffle
from random import choice
import kitty_lacey_for_calling
import time

def braid_to_e1(braid, number_of_rows):
  e1 = []
  for row_number in range(1, number_of_rows+1):
    row = []
    for crossing in braid:
      if abs(crossing) == row_number:
        if crossing > 0:
          row.append(1)
        else:
          row.append(-1)
      else:
        row.append(0)
    e1.append(row)
  return e1

def e1_to_e2(braid):
  new_braid = [ [0 for _ in range(len(braid[0]))] for _ in range(len(braid)+1)]
  for i in range(len(braid)):
      for j in range(len(braid[0])):
          if braid[i][j] == 1:
              new_braid[i][j] = 1
              new_braid[i+1][j] = -1
          if braid[i][j] == -1:
              new_braid[i][j] = -1
              new_braid[i+1][j] = 1
  # now braid is the standard encoding e1, and new_braid is e2
  return new_braid

def braid_to_e2(braid, n):
  return e1_to_e2(braid_to_e1(braid, n))

def e1_to_e3(braid):
  new_braid = [ [0 for _ in range(len(braid[0]))] for _ in range(len(braid)+1)]
  for i in range(len(braid)):
      for j in range(len(braid[0])):
          if braid[i][j] == 1:
              new_braid[i][j] = 1
              new_braid[i+1][j] = -1
          if braid[i][j] == -1:
              new_braid[i][j] = -1
              new_braid[i+1][j] = 1
  # now braid is the standard encoding e1, and new_braid is e2
  permutation = list(range(len(new_braid)))
  for j in range(len(braid[0])):
      # act with the permutation on the i-th column in new_braid
      column = [new_braid[i][j] for i in range(len(new_braid))]
      #column = [column[permutation[i]] for i in range(len(new_braid))]
      column = [column[permutation.index(i)] for i in range(len(new_braid))]
      for i in range(len(new_braid)):
          new_braid[i][j] = column[i]
      # update the permutation using braid
      column = [braid[i][j] for i in range(len(braid))]
      if 1 in column:
          i = column.index(1)
      else:
          i = column.index(-1)
      permutation[i], permutation[i+1] = permutation[i+1], permutation[i]
  #print(flatten(new_braid, label), file=output_file)
  return new_braid

def braid_to_e3(braid, n):
  return e1_to_e3(braid_to_e1(braid, n))

def alternating_sum(l):
  return sum(l[::2]) - sum(l[1::2])

def flatten(matrix, label):
    to_print = matrix + [[label]]
    return ', '.join([str(a) for a in list(itertools.chain(*to_print))])

def modify_e3(e3):
  for i in range(len(e3[0])):
    # in column i, find 0
    j = [e3[0][i], e3[1][i], e3[2][i]].index(0)
    j = (j-1+3) % 3
    e3[j][i] = 0
  return e3

def is_cep(braid, c, t):
    # list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    # braid = [choice(list_of_possible_crossings) for _ in range(kitty_lacey_for_calling.braid_len)]
    s_0 = time.time()
    e1 = braid_to_e1(braid, 3)
    s = sum(sum(row) for row in e1)
    if s != 0:
        cep = False
    else:
        c[0] += 1
        cep = True
    e_0 = time.time()
    t[0] += e_0 - s_0  
    return  cep, c, t

def is_ces(braid, c, t):
    # list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    # braid = [choice(list_of_possible_crossings) for _ in range(kitty_lacey_for_calling.braid_len)]
    s_1 = time.time()
    e1 = braid_to_e1(braid, 3)
    e3 = e1_to_e3(e1)
    alt_sums = [alternating_sum(strand) for strand in e3]
    if not all([s == 0 for s in alt_sums]): 
        ces = False
    else:
        c[1] += 1
        ces = True
    e_1 = time.time()
    t[1] += e_1 - s_1 
    return ces, c, t

def is_ces_m(braid, c, t):
    # list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    # braid = [choice(list_of_possible_crossings) for _ in range(kitty_lacey_for_calling.braid_len)]
    s_1 = time.time()
    e1 = braid_to_e1(braid, 3)
    e3 = e1_to_e3(e1)
    modify_e3(e3)
    alt_sums = [alternating_sum(strand) for strand in e3]
    if not all([s == 0 for s in alt_sums]): 
         ces_m = False
    else:
        c[2] += 1
        ces_m = True
    e_1 = time.time()
    t[2] += e_1 - s_1 
    return  ces_m, c, t

def is_aut(braid, c, t):
    # list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    # braid = [choice(list_of_possible_crossings) for _ in range(kitty_lacey_for_calling.braid_len)]
    s_2 = time.time()
    if kitty_lacey_for_calling.is_trivial(braid):
        c[3] += 1
        triv = True
    else:
        triv = False
    e_2 = time.time()
    t[3] += e_2 - s_2 
    t[4] = e_2 - s_2 
    return triv, c, t

# def is_trivial(braid, c, t):
#     # list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
#     # braid = [choice(list_of_possible_crossings) for _ in range(kitty_lacey_for_calling.braid_len)]
#     s_0 = time.time()
#     e1 = braid_to_e1(braid, 3)
#     s = sum(sum(row) for row in e1)
#     if s != 0:
#         # e_0 = time.time()
#         return  c, t
#     else:
#         e_0 = time.time()
#         t[0] += e_0 - s_0  
#         c[0] += 1
#     #####
#     s_1 = time.time()
#     e3 = e1_to_e3(e1)
#     alt_sums = [alternating_sum(strand) for strand in e3]
#     if not all([s == 0 for s in alt_sums]): 
#         # e_1 = time.time()
#         return c, t
#     else:
#         e_1 = time.time()
#         c[1] += 1
#         t[1] += e_1 - s_1 
    
#     s_2 = time.time()
#     if kitty_lacey_for_calling.is_trivial(braid):
#         e_2 = time.time()
#         c[2] += 1
#         t[2] += e_2 - s_2 
#         t[3] = e_2 - s_2 
#         return c, t
#     else:
#         e_2 = time.time()
#         t[2] += e_2 - s_2 
#         t[3] = e_2 - s_2 
#         return c, t
# s = time.time()
# kitty_lacey_for_calling.is_trivial([-2, 2, 1, 1, -2, 2, -2, -1, -1, -2, -2, -2, 1, 1, 1, 2, -1, 1, 2, 1, -2, 2, -1, -1, -1, -1, 2, 2, -2, -1, -2, -2, 1, 2, 1, -1, -1, -2, 1, 1, 1, -1, 1, 1, 2, 2, -1, -1, -2, 1])
# e = time.time()
# print(e-s)    
    
    # e_1 = time.time()
    # if s == 0 and all([s == 0 for s in alt_sums]):
    #     # c[2] += 1
    #     pass