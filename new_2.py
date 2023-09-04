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

def is_trivial(braid, c):
    # list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
    # braid = [choice(list_of_possible_crossings) for _ in range(kitty_lacey_for_calling.braid_len)]
    e1 = braid_to_e1(braid, 3)
    #print(e1)
    ces_m, cep_ces = False, False
    su = sum(sum(row) for row in e1)
    if su != 0:
        pass
    else:
        c[0] += 1
    e3 = e1_to_e3(e1)
    alt_sums = [alternating_sum(strand) for strand in e3]
    if not all([s == 0 for s in alt_sums]): 
        pass
    else:
        c[1] += 1
    if su == 0 and all([s == 0 for s in alt_sums]):
        c[2] += 1
        cep_ces = True
    e4 = modify_e3(e3)
    alt_sums_e4 = [alternating_sum(strand) for strand in e4]
    if not all([s == 0 for s in alt_sums_e4]): 
        pass
    else:
        c[3] += 1
        ces_m = True
    if ces_m and cep_ces:
        c[6] += 1
    if su == 0 and all([s == 0 for s in alt_sums_e4]):
        c[4] += 1
    if kitty_lacey_for_calling.is_trivial(braid):
        c[5] += 1
        return False, c
    else:
        # c[3] += 1
        return True, c

# number_of_braids_of_each_kind = 1000
# n = kitty_lacey_for_calling.strands_in_braid - 1
# trivial_braids = []
# non_trivial_braids = []



# while len(trivial_braids) < number_of_braids_of_each_kind or len(non_trivial_braids) < number_of_braids_of_each_kind:
#   list_of_possible_crossings = list(range(-n, 0)) + list(range(1, n+1))
#   braid = [choice(list_of_possible_crossings) for _ in range(kitty_lacey_for_calling.braid_len)]
#   #print(kitty_lacey_for_calling.is_trivial(braid))
#   #if not kitty_lacey_for_calling.is_trivial(braid): continue
#   # the braid (currently represented as a list) is trivial
#   #print(braid, kitty_lacey_for_calling.is_trivial(braid))
#   e1 = braid_to_e1(braid, n)
#   #print(e1)
#   s = sum(sum(row) for row in e1)
#   if s != 0: continue
#   e3 = e1_to_e3(e1)
#   #print(e3)
#   alt_sums = [alternating_sum(strand) for strand in e3]
#   #print(alt_sums)
#   if not all([s == 0 for s in alt_sums]): continue
#   #print(alt_sums)
#   #print(e3)
#   #print(braid, kitty_lacey_for_calling.is_trivial(braid))
#   #print(alt_sums)
#   if kitty_lacey_for_calling.is_trivial(braid):
#     if not braid in trivial_braids and len(trivial_braids) < number_of_braids_of_each_kind:
#       trivial_braids.append(braid)
#   else:
#     if not braid in non_trivial_braids and len(non_trivial_braids) < number_of_braids_of_each_kind:
#       non_trivial_braids.append(braid)
# #print('trivial', trivial_braids)
# #print('non-trivial', non_trivial_braids)
# output_file_prefix = "C:\\Box\\Braids\\trivial-and-not-braids\\centre\\centre2-12-3-2000"
# # create file with e1
# output_file = output_file_prefix + '-e1.txt'
# with open(output_file, "w") as output_file:
#   for braid in trivial_braids:
#     label = 1
#     e1 = braid_to_e1(braid, n)
#     print(flatten(e1, label), file=output_file)
#   for braid in non_trivial_braids:
#     label = 0
#     e1 = braid_to_e1(braid, n)
#     print(flatten(e1, label), file=output_file)
# # create file with e2
# output_file = output_file_prefix + '-e2.txt'
# with open(output_file, "w") as output_file:
#   for braid in trivial_braids:
#     label = 1
#     e2 = braid_to_e2(braid, n)
#     print(flatten(e2, label), file=output_file)
#   for braid in non_trivial_braids:
#     label = 0
#     e2 = braid_to_e2(braid, n)
#     print(flatten(e2, label), file=output_file)
# # create file with e3
# output_file = output_file_prefix + '-e3.txt'
# with open(output_file, "w") as output_file:
#   for braid in trivial_braids:
#     label = 1
#     e3 = braid_to_e3(braid, n)
#     print(flatten(e3, label), file=output_file)
#   for braid in non_trivial_braids:
#     label = 0
#     e3 = braid_to_e3(braid, n)
#     print(flatten(e3, label), file=output_file)

'''
output_file = "C:\\Box\\Braids\\trivial-and-not-braids\\centre.txt"
L = 12
half_len = L // 2

def create_half_braid_in_e3():
  columns = []
  for i in range(half_len):
    column = [-1, 1, 0]
    shuffle(column)
    #print(column)
    columns.append(column)
  half_braid = [*zip(*columns)]
  #print(half_braid)
  return half_braid

def alternating_sum(l):
  return sum(l[::2]) - sum(l[1::2])

def alternating_sum_of_braid(braid):
  #print([[strand[::2], strand[1::2]] for strand in braid])
  return [sum(strand[::2]) - sum(strand[1::2]) for strand in braid]

hb = create_half_braid_in_e3()
print(hb)
print(alternating_sum_of_braid(hb))

def create_braid_in_centre_in_e3():
  pass
'''  

'''
#filename = "C:\\Box\\Braids\\trivial-and-not-braids\\trivial-and-not-braids-10-3-2000.csv"
#print(filename)
folder = "C:\\Box\\Braids\\trivial-and-not-braids\\"

def flatten(matrix, label):
    to_print = matrix + [[label]]
    return ', '.join([str(a) for a in list(itertools.chain(*to_print))])

def create_e1(filename):
    # e1 is the standard encoding
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        output_file = filename[:-4] + '-e1.txt'
        with open(output_file, "w") as output_file:
            for row in reader:
                braid = row['braid']
                label = row['label']
                #print(braid, label)
                braid = braid.replace("  ", ",")
                braid = braid.replace(" -", ",-")
                braid = braid.replace("\n", ",")
                braid = braid.replace(" ", ",")
                braid = braid.replace(",,", ",")
                braid = braid.replace("[,", "[")
                #print(braid)
                braid = eval(braid)
                label = eval(label)
                print(flatten(braid, label), file=output_file)
                #break
     
def create_e2(filename):
    # e2 is encoding as matrices with row per strand and column per crossing, with +1 and -1
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        output_file = filename[:-4] + '-e2.txt'
        with open(output_file, "w") as output_file:
            for row in reader:
                braid = row['braid']
                label = row['label']
                #print(braid, label)
                braid = braid.replace("  ", ",")
                braid = braid.replace(" -", ",-")
                braid = braid.replace("\n", ",")
                braid = braid.replace(" ", ",")
                braid = braid.replace(",,", ",")
                braid = braid.replace("[,", "[")
                braid = eval(braid)
                label = eval(label)
                new_braid = [ [0 for _ in range(len(braid[0]))] for _ in range(len(braid)+1)]
                for i in range(len(braid)):
                    for j in range(len(braid[0])):
                        if braid[i][j] == 1:
                            new_braid[i][j] = 1
                            new_braid[i+1][j] = -1
                        if braid[i][j] == -1:
                            new_braid[i][j] = -1
                            new_braid[i+1][j] = 1
                print(flatten(new_braid, label), file=output_file)
                #print(braid)
                #print([new_braid, label])
                #break

def create_e3(filename):
    # e3 is encoding as matrices with row per strand and column per crossing, with +1 and -1, with the order of strands preserved
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        output_file = filename[:-4] + '-e3.txt'
        with open(output_file, "w") as output_file:
            for row in reader:
                braid = row['braid']
                label = row['label']
                #print(braid, label)
                braid = braid.replace("  ", ",")
                braid = braid.replace(" -", ",-")
                braid = braid.replace("\n", ",")
                braid = braid.replace(" ", ",")
                braid = braid.replace(",,", ",")
                braid = braid.replace("[,", "[")
                braid = eval(braid)
                label = eval(label)
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
                    #print(permutation)
                #print(braid)
                #print([new_braid, label])
                print(flatten(new_braid, label), file=output_file)
                #break

for file in os.listdir(folder):
    if file.endswith(".csv"):
        filename = os.path.join(folder, file)
        print(filename)
        create_e1(filename)
        create_e2(filename)
        create_e3(filename)
'''

'''
filename = "C:\\Box\\Braids\\trivial-and-not-braids\\trivial-and-not-braids-10-3-2000-e3.txt"
filename = "C:\\Box\\Braids\\trivial-and-not-braids\\trivial-and-not-braids-18-3-10000-e3.txt"

def alternating_sum(l):
  return sum(l[::2]) - sum(l[1::2])

with open(filename) as file:
    count_examples = 0
    while line := file.readline():
        #print(line.rstrip())
        instance = [int(s) for s in line.split(',')]
        #print(instance)
        braid = instance[:-1]
        trivial = instance[-1]
        #print(len(braid), trivial)
        if trivial == 1: continue
        #if 2 * alternating_sum(braid[:10]) + alternating_sum(braid[10:20]) - 2 * alternating_sum(braid[20:]) != 0: continue
        if alternating_sum(braid[:10]) - alternating_sum(braid[20:]) != 0: continue
        #if alternating_sum(braid[:10]) != 0: continue
        #if alternating_sum(braid[10:20]) != 0: continue
        #if alternating_sum(braid[20:]) != 0: continue
        #print(alternating_sum(braid[:10]), alternating_sum(braid[10:20]), alternating_sum(braid[20:]), trivial)
        #print(braid)
        
        #print(braid[:10])
        #print(braid[10:20])
        #print(braid[20:])
        #print()
        
        count_examples += 1
    print(count_examples)
'''        
