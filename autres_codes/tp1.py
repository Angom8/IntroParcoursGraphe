import tsplib95


choix = input("Fichier : ")


problem = tsplib95.load(choix + ".tsp")

print(problem.edge_weights)
cities = len(list(problem.get_nodes()))

i = int(input("Insérer une ville, de 0 à " + str(cities - 1) + " : "))

assert(i<=cities)

path = []
path.append(i)
dist = 0
first = i
current_min = 10000000
current_imin = 0

while(cities > len(path)):
	k=0
	print("TOUR " + str(len(path)))
	while(k<cities):
		if(path.count(k) == 0):
			print(k)
			edge = i, k
			current_min = min(problem.get_weight(*edge), current_min)
			if(problem.get_weight(*edge) == current_min and current_min != problem.get_weight(i, current_imin)):
				current_imin = k
		k+=1
	dist += current_min
	path.append(current_imin)
	i = current_imin
	current_min = 10000000
dist += problem.get_weight(*(i, first))
print(dist)
path.append(first)
print(path)
