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
current_max = 0
current_imax = 0

while(cities > len(path)):
	k=0
	print("TOUR " + str(len(path)))
	while(k<cities):
		if(path.count(k) == 0):
			print(k)
			edge = i, k
			current_max = max(problem.get_weight(*edge), current_max)
			if(current_max != problem.get_weight(i, current_imax)):
				current_imax = k
		k+=1
	dist += current_max
	path.append(current_imax)
	i = current_imax
dist += problem.get_weight(*(i, first))
print(dist)
path.append(first)
print(path)
