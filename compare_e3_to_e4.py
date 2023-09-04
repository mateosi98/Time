import csv
import itertools
import os
from random import shuffle
from random import choice
import kitty_lacey_for_calling

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

def modify_e3(e3):
  for i in range(len(e3[0])):
    # in column i, find 0
    j = [e3[0][i], e3[1][i], e3[2][i]].index(0)
    j = (j-1+3) % 3
    e3[j][i] = 0
  return e3

def braid_to_e3(braid, n):
  return e1_to_e3(braid_to_e1(braid, n))

def alternating_sum(l):
  return sum(l[::2]) - sum(l[1::2])

def flatten(matrix, label):
    to_print = matrix + [[label]]
    return ', '.join([str(a) for a in list(itertools.chain(*to_print))])

n = 2
braid = [1, 2, 1, 2, 1, 2]
print('compare e3 and modified e3 (e4) on an example of one braid', braid)
e1 = braid_to_e1(braid, n)
e3 = e1_to_e3(e1)
#print(e3)
sums_e3 = [alternating_sum(row) for row in e3]
#if all([s == 0 for s in sums_e3]): continue
modify_e3(e3)
e4 = e3
#print(e4)
sums_e4 = [alternating_sum(row) for row in e4]
#if not all([s == 0 for s in sums_e4]): continue
print(braid, e4)
print(sums_e3, sums_e4)

strands_in_braid = 3
braid_len = 20
print('compare e3 and modified e3 (e4) on an example of randomly chosen braids of length', braid_len)
n = strands_in_braid - 1
list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
gap_between_e3_and_e4 = 0
for _ in range(1000):
  braid = [choice(list_of_possible_crossings) for _ in range(braid_len)]
  e1 = braid_to_e1(braid, n)
  e3 = e1_to_e3(e1)
  #print(e3)
  sums_e3 = [alternating_sum(row) for row in e3]
  if not all([s == 0 for s in sums_e3]): continue
  modify_e3(e3)
  e4 = e3
  #print(e4)
  sums_e4 = [alternating_sum(row) for row in e4]
  if all([s == 0 for s in sums_e4]): continue
  print(braid, e4)
  print(sums_e3, sums_e4)
  gap_between_e3_and_e4 += 1
print(gap_between_e3_and_e4)
