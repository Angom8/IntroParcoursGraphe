
import random
import string
import numpy as np
from deap import base, creator, tools, algorithms

def f(x,y):
    return (1-x)*(1-x) + 100*(y-x*x)*(y-x*x)

        
        
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

## globals,

random.seed(11);
np.random.seed(121);


INDIVIDUAL_SIZE = NUMBER_OF_CITIES = 100
POPULATION_SIZE = 200
N_ITERATIONS = 1000
N_MATINGS = 50
            
toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, -1000, 1000)

## permutation setup for individual,

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_int, 2)

## population setup,
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def EVALUATE(individual):
    x = individual[0]
    y = individual[1]
    return (1-x)*(1-x) + 100*(y-x*x)*(y-x*x)

toolbox.register("evaluate", EVALUATE)

toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=10)

algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=50)


