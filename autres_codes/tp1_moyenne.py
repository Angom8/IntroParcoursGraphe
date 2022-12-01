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
current_mmin = 10000000
current_imin = 0

while(cities > len(path)):
	k=0
	tab = []
	print("TOUR " + str(len(path)))
	moyenne = 0
	compte = 0
	while(k<cities):
		if(path.count(k) == 0):
			moyenne += problem.get_weight(*(i, k))
			compte += 1
		tab.append((problem.get_weight(*(i, k))))
		k+=1
	moyenne = moyenne/compte
	print("Moyenne : " + str(moyenne))
	k = 0
	while(k<cities):
		if(path.count(k) == 0):
			moyenne_dif = abs(moyenne - tab[k])
			current_mmin = min(moyenne_dif, current_mmin)
			if(moyenne_dif == current_mmin):
				current_imin = k
				current_min = tab[k]
		k+=1	
	print("Resultat choisi : " + str(current_min))
	dist += current_min
	path.append(current_imin)
	i = current_imin
	current_min = 10000000
	current_mmin = 10000000
dist += problem.get_weight(*(i, first))
print(dist)
path.append(first)
print(path)
