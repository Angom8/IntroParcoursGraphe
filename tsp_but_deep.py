import tsplib95
import random
import math
import matplotlib.pyplot as plt
import csv

from deap import base
from deap import creator
from deap import tools

#FILE LOADING
choix = input("Fichier (sans l'extension) : ")
quick = input("Quick mode ? Y/N : ")
l_quick = -1
l_quick_confirm = True
l_quick_count = 0
problem = tsplib95.load(choix + ".tsp")
nb_cities =  len(list(problem.get_nodes()))
evaluations = 0


# VARIABLES et CST
CXPB = 0.75 #cross
MUTPB = 0.25 #prob mutation
GMAX = 500 #nb generations
NPOP = 100 #taille pop
LQUICKSTACK = 10 #nb valeurs identiques avant arret


#GENERER LES INDIVIDUS
def gen_individual(x):
    l = list(range(x))
    random.shuffle(l)
    return l

#RETOURNE SOMME DES DISTANCES INDIVIDU
def sum_tsp(value):
    s = 0
    for v in range(len(value) - 1):
        s += problem.get_weight(   *(value[v], value[v + 1])   )
    s += problem.get_weight(   *(value[v], value[v + 1])   )
    return s

#EVALUATION D'UN INDIVIDU (plante si utilisation directe de evaluate)
def evaluate_one(individual):
    return evaluate(individual),

#EVALUATION
def evaluate(value):
    s = 0
    for v in range(len(value) - 1):
        s += problem.get_weight(   *(value[v], value[v + 1])   )
    s += problem.get_weight(   *(value[v], value[v + 1])   )
    global evaluations
    evaluations += 1
    return s


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

#TOOLBOX D'EUDIPE
toolbox = base.Toolbox()
toolbox.register("cities", gen_individual, nb_cities)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.cities)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_one)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

#ECRITURE DU FICHIER + EVOLUTION
with open('tsp_results.csv', 'w') as csvfile:


    output = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    pop = toolbox.population(NPOP)

    #Génération de la première population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    fits = [ind.fitness.values[0] for ind in pop]

    generation = 1
    output.writerow(['Generation', 'Min', 'Max', 'Average', 'Stddeviation'])
   
    while generation < GMAX and l_quick_confirm:
      
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

	#Traitement de l'évolution avec création des enfants à partir des parents par sélection des meilleurs au score minimal
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)

        z_temp = zip(invalid_ind, fitnesses)
        for ind, fit in z_temp:
            ind.fitness.values = fit

	
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]

	#Calcul des stats
        length = len(pop)
        mean = sum(fits) / length
        sum_sqr = sum(x*x for x in fits)
        std = math.sqrt(abs(sum_sqr/length-mean**2))

	#Ecriture du CSV
        output.writerow([generation, min(fits), max(fits), mean, std])
        
       
        #Traitement du quick mode
        if(quick == "Y" or quick =="y"):
        	if(l_quick == min(fits)):
        		l_quick_count += 1
        	else:
        		l_quick_count = 0
        	if(l_quick_count > LQUICKSTACK):
        		l_quick_confirm = False
        	l_quick = min(fits)
        
        generation += 1


    solution = min(pop, key=lambda a: a.fitness.values[0])
    print(f"Parcours obtenu : {solution}")
    print(f"Nombre d'évaluations : {evaluations}")
    print(f"Distance parcourue : {sum_tsp(solution)}")
