import tsplib95
from random import *
import copy

#FILE LOADING
choix = input("Fichier (sans l'extension) : ")
problem = tsplib95.load(choix + ".tsp")
cities =  len(list(problem.get_nodes()))

#GLOBAL VALUES INIT
impossible = 10000000
nb_essais_trouver_sol = 1000
nb_essais_amelio = 1000
nb_tour_amelio = 10

#SWAP
"Inverse deux villes au hasard dans la liste du parcours (exceptée la ville de départ)"
def swap(t):

	i = randint(1, len(t)-2)
	j = randint(1, len(t)-2)
	z = t[i]
	t[i] = t[j]
	t[j] = z
	
	
#COMPLETE SWAP
"Change complétement le parcours à partir d'une ville choisie au hasard"
def heavy_swap(t, z):

    r_cities = []

    if(z != 0):
    	i = 0
    	while(i < z):
    		r_cities.append(t[i])
    		i+=1
    
    r_cities_tmp = sample(t[z:-1], len(t[z:-1]))
    
    
    if(z != 0):
    	i = z
    	j = 0
    	while(i < len(t)-1):
    		r_cities.append(r_cities_tmp[j])
    		i+=1
    		j+=1
    else:
    	r_cities= r_cities_tmp
    
    start = r_cities.index(t[0])
    r_cities[0], r_cities[start] = r_cities[start], r_cities[0]
    r_cities.append(t[0])

    return r_cities	
	
#RECALC
"Recalcule l'ensemble des distances"
def recalc(t):
	dist = 0
	for u in range(len(t)-1):
		dist += problem.get_weight(*(t[u], t[u+1]))
		
	return dist
	
#DETERMINATION SOL ALEATOIRE
"Détermine un chemin au hasard selon un certain nombre d'essais et prend le meilleur"
def fullrandom() :
	i = int(input("Insérer une ville, de 0 à " + str(cities - 1) + " : "))
	z = 0
	zlist = []
	zdist = impossible 


	while(z < nb_essais_trouver_sol):
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
		
		if(min(zdist, dist) == dist):
			zdist = dist
			zlist = path
			
		z += 1
		
	return zlist , zdist
	
#PAR PROCHE EN PROCHE
"Prend la ville la plus proche"
def proche_en_proche():
	i = int(input("Insérer une ville, de 0 à " + str(cities - 1) + " : "))
	path = []
	path.append(i)
	dist = 0
	first = i
	current_min = impossible
	current_imin = 0

	while(cities > len(path)):
		k=0
		while(k<cities):
			if(path.count(k) == 0):
				edge = i, k
				current_min = min(problem.get_weight(*edge), current_min)
				if(problem.get_weight(*edge) == current_min and current_min != problem.get_weight(i, current_imin)):
					current_imin = k
			k+=1
		dist += current_min
		path.append(current_imin)
		i = current_imin
		current_min = impossible
	dist += problem.get_weight(*(i, first))
	path.append(first)
	return path, dist

#PAR MOYENNE
"Fais une moyenne de toutes les distances et prend la ville dont la distance est la plus proche de cette moyenne"
def parmoyenne():
	i = int(input("Insérer une ville, de 0 à " + str(cities - 1) + " : "))
	path = []
	path.append(i)
	dist = 0
	first = i
	current_min = impossible
	current_mmin = impossible
	current_imin = 0

	while(cities > len(path)):
		k=0
		tab = []
		moyenne = 0
		compte = 0
		while(k<cities):
			if(path.count(k) == 0):
				moyenne += problem.get_weight(*(i, k))
				compte += 1
			tab.append((problem.get_weight(*(i, k))))
			k+=1
		moyenne = moyenne/compte
		k = 0
		while(k<cities):
			if(path.count(k) == 0):
				moyenne_dif = abs(moyenne - tab[k])
				current_mmin = min(moyenne_dif, current_mmin)
				if(moyenne_dif == current_mmin):
					current_imin = k
					current_min = tab[k]
			k+=1	
		dist += current_min
		path.append(current_imin)
		i = current_imin
		current_min = impossible
		current_mmin = impossible
	dist += problem.get_weight(*(i, first))
	path.append(first)
	
	return path, dist
	
#PAR MAX
"Prend la ville la plus éloignée"
def parmax():
	i = int(input("Insérer une ville, de 0 à " + str(cities - 1) + " : "))
	path = []
	path.append(i)
	dist = 0
	first = i
	current_max = 0
	current_imax = 0

	while(cities > len(path)):
		k=0
		while(k<cities):
			if(path.count(k) == 0):
				edge = i, k
				print(edge)
				current_max = max(problem.get_weight(*edge), current_max)
				if(current_max != problem.get_weight(i, current_imax)):
					current_imax = k
			k+=1
		dist += current_max
		path.append(current_imax)
		i = current_imax
	dist += problem.get_weight(*(i, first))
	path.append(first)
	return path, dist
	
#zlist, zdist = parmax()
#zlist, zdist = parmoyenne()
#zlist, zdist = fullrandom()
zlist, zdist = proche_en_proche()

print(zlist)
print(recalc(zlist))
print(zdist)
ptemp = copy.deepcopy(zlist)
pptemp = []
dtemp = zdist
z = -1
g = 0

while(z == -1 or zdist > dtemp or g < nb_tour_amelio):

	zdist = dtemp
	z = 0
	
	while(z < nb_essais_amelio ):
		pptemp = copy.deepcopy(ptemp)
		pptemp = heavy_swap(pptemp, randint(0, cities-1))

		if(recalc(pptemp) < dtemp):
			dtemp = recalc(pptemp)
			ptemp = copy.deepcopy(pptemp)

		z+=1
		
	if(zdist == dtemp):
		g+=1
		print(dtemp)

			
print(ptemp)
print(str(zdist))	


