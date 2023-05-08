# GENETIC ALGORITHM

import copy
import random
import numpy as np

bestSol_path = []
bestSol_cost = np.inf

isEuclidean = 1 if input() == 'EUCLIDEAN' else 0
n = int(input())  # use this to set the max_limit for the first time gen_sol function

coordinates=[]
for i in range(n):
  coordinates.append([ float(x) for x in input().split(' ')])

distances = []
for i in range(n):
  distances.append([ float(x) for x in input().split(' ')])


def findMin(city,path):
  x = city.index(min(city))
  if x not in path :
    return x
  else :
    city[x]=99999
    return findMin(city,path)

def nnh(start,distances):
  tsp=copy.deepcopy(distances)
  totalCost=0
  path=[start]
  currentCityDistances=tsp[start]
  for i in range(len(tsp)-1):
    minCity=findMin(currentCityDistances,path)
    path.append(minCity)
    totalCost+=currentCityDistances[minCity]
    currentCityDistances=tsp[minCity]
  return path,totalCost

mincost=9999
optimal_path=[]
seen=[]
for i in range(10):
  node=random.randint(0,len(distances)-1)
  if node in seen : continue
  seen.append(node)
  path,cost=nnh(node,distances)
  if cost < mincost:
    optimal_path=path
    mincost=cost

print(optimal_path)

def list_to_tuple(list_of_lists):
    return tuple(tuple(item) for item in list_of_lists)

# tsp = list_to_tuple(distances)

def pathCost(path,tsp):
  cost = 0
  startCity = path[0]
  for i in path[1:] : 
    cost = cost + tsp[startCity][i]
    startCity = i
  return cost

def gen_sol(tsp,max_limit):

  solutions = []
  for i in range(max_limit):
    solutions.append(randomSolution(tsp))

  rankedSolution = []
  for i in range(max_limit):
    rankedSolution.append((pathCost(solutions[i],tsp),solutions[i]))
  rankedSolution.sort()

  return rankedSolution 

def getCycle(path1, path2, idx):
    cycle = [idx]
    visited = set(cycle)

    while True:
        val = path2[idx]
        idx = path1.index(val)

        if idx in visited:
            break

        cycle.append(idx)
        visited.add(idx)

    return cycle

def cycleCross(path1,path2):
  idx, i = 0 , 0
  even_list, odd_list = [],[]
  while len(even_list + odd_list) < len(path1):
    temp_cycle = getCycle(path1,path2,idx) 
    if i % 2 == 0 : even_list.extend(temp_cycle) 
    if i % 2 != 0 : odd_list.extend(temp_cycle)
    i = i + 1
    for j in range(idx,len(path1)): 
      if j not in even_list+odd_list : 
        idx = j
        break

  off_even_1 = copy.deepcopy(path1)
  off_even_2 = copy.deepcopy(path1)
  off_odd_1 = copy.deepcopy(path2)
  off_odd_2 = copy.deepcopy(path2)
  for m in even_list :
    off_even_1[m] = path2[m]
    off_odd_2[m] = path1[m]
  for m in even_list :
    off_odd_1[m] = path2[m]
    off_even_2[m] = path1[m]

  return [off_even_1,off_even_2, off_odd_1, off_odd_2]

def do_crossing(population,distances):
  new_pop = []
  
  for i in range(random.randint(50,500)):
    random_path_1 = random.choice(population)
    random_path_2 = random.choice(population)
    new_pop.extend(cycleCross(random_path_1[1],random_path_2[1]))

  for j in population[:20]:  
    for i in population[:10]:
      new_pop.extend(cycleCross(j[1],i[1]))

  for i,j in zip(population,population[1:40]):
    new_pop.extend(cycleCross(i[1],j[1]))

  ranked_new_pop = []
  for i in new_pop :
    ranked_new_pop.append((pathCost(i,distances),i))
  ranked_new_pop.sort()

  return ranked_new_pop

def targeted_crossing(population,distances):      #10 path only
  new_pop = []
  for j in population:  
    for i in population:
      new_pop.extend(cycleCross(j[1],i[1]))

  ranked_new_pop = []
  for i in new_pop :
    ranked_new_pop.append((pathCost(i,distances),i))
  ranked_new_pop.sort()

  return ranked_new_pop

for i in range(5):
    population = gen_sol(distances,100*n)    # make it of the order of input n
    population = population[:300]

    if population[0][0] < bestSol_cost:
        bestSol_cost = population[0][0]
        bestSol_path = population[0][1]
        print(bestSol_path)     #every time it's updated print it 

    for i in range(5):
        x = do_crossing(population,distances)
        if x[0][0] < bestSol_cost:
            bestSol_cost = x[0][0]
            bestSol_path = x[0][1]
            print(bestSol_path)

    y = targeted_crossing(x[:50],distances)
    if y[0][0] < bestSol_cost:
        bestSol_cost = x[0][0]
        bestSol_path = x[0][1]
        print(bestSol_path)
    
    population = y