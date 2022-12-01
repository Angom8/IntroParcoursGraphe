import tsplib95
from random import *

problem = tsplib95.load('gr7.tsp')

print(problem.edge_weights)
cities = len(list(problem.get_nodes()))

i = int(input("Insérer une ville, de 0 à " + str(cities - 1) + " : "))

assert(i<=cities)

z = 0
zlist = []
zdist = 0


while(z < 1000):
	path = []
	path.append(i)
	dist = 0
	first = i
	lk = i
	while(cities > len(path)):

		k = randint(0, cities-1)
		while(path.count(k) != 0):
			k = randint(0, cities-1)
		dist += problem.get_weight(*(lk, k))
		path.append(k)
		lk = k
		
	dist += problem.get_weight(*(path[cities-1], first))
	path.append(first)
	
	zdist += dist
		
	z += 1
	
print(zdist/1000)
