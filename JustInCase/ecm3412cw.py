import numpy as np
import matplotlib.pyplot as plt
import random

# 1. Initialize a population of chromosomes (solutions).
# make a population function that takes bin and weight and generates a population for bpp1 and bpp2
def initialize_population(bin_count, weights, population_size=100):
    population = []

    for _ in range(population_size):
        # generate chromosomes of random values from 1 to bin count, and length is the same for weights and chromosomes
        chromosome = np.random.randint(1, bin_count + 1, size=len(weights), dtype=np.int64)
        population.append(chromosome)

    return population

# 2. Evaluate the fitness of each chromosome in the population.
def evaluate_population(population, bin_count, weights):
# loop thru each chromosome in the population
    fitness = []
    for cs in population:
        # initialise list that holds each bin weight for each chromosome
        bins = [0]*bin_count
        for i in range(bin_count):
            bins.append(0)
        # loop thru each item, add their weight into their bin
        for i in range(len(weights)):
            bins[cs[i] - 1] += weights[i]
    
        # Sort and calc fitnes
        max_bin = max(bins)
        min_bin = min(bins)

        d = max_bin - min_bin
        fitness.append(100.0 / (1.0 + float(d)))

    return fitness

# 3. Select parents for reproduction using selection method - Tournament selection
def tournament_select(population, fitness, t):
    fitnesses = []
    indices = []
    # 1. Randomly select t chromosomes from the population (tournament size)
    for _ in range(t): 
        index = random.randint(0, len(population) - 1) # select random chromosome
        fitnesses.append(fitness[index]) # add their fitness into fitnesses list
        indices.append(index) 
        
    # 2. Choose the chromosome with the best fitness from this tournament
    best_fitness = max(fitnesses)
    best_chromosome = indices[fitnesses.index(best_fitness)]

    return best_chromosome
    # 3. Repeat to select second parent - made a helper function
def find_two_parents(population, fitness, t):
    p1_idx = tournament_select(population, fitness, t)
    p2_idx = tournament_select(population, fitness, t)

    parent1 = population[p1_idx]
    parent2 = population[p2_idx] # this will return the actual chromosome so itll be easier for mutation function
    
    return parent1, parent2

# 4. Create offspring through crossover and mutation operations.
def mutate_gene(chromosome, pm, bin_count):
    child = chromosome.copy()
    # 1. For each gene, with probability pm (mutation rate)
    for i,gene in enumerate(chromosome):
        if np.random.rand() < pm: # mutation probability
            # find another bin count that isnt itself
            new_gene = gene 
            while new_gene == gene: # this loop ensures the new mutation isnt the old bin value 
    # 2. Randomly change the bin assignment to any valid bin (1 to b)
                new_gene = np.random.randint(1, bin_count+1)

            child[i] = new_gene
    return child


def crossover_genes(parent1, parent2, pc=0.8):
# 3. Apply crossover with probability pc (crossover rate)
    if np.random.rand() < pc:
        child1, child2 = [],[]
        # 1. For each gene position, flip a coin
        for i in range(len(parent1)):
            if random.choice([True, False]):
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        # 2. If heads, take gene from parent 1; if tails, take gene from parent 2
        return np.array(child1, dtype=np.int64), np.array(child2, dtype=np.int64)
    else: # not pc, thus just return p1 and p2 as c1 and c2
        return parent1.copy(), parent2.copy()

# 5. Replace the old population with the new population (or subset).
# Population Replacement: Use generational replacement where the entire population is replaced each
# generation, except keep the best chromosome from the previous generation (elitism).
def get_elite_gene(population, fitness):
    best_idx = np.argmax(fitness) # get the best fitness' index
    elite = population[best_idx].copy() # get that index's full gene
    return elite, fitness[best_idx]

def generate_new_population(population, fitness, bin_count, t, pm, pc):
    elite, elite_fit = get_elite_gene(population, fitness)
    new_population = [elite]

    while len(new_population) < len(population):
        p1_idx = tournament_select(population, fitness, t)
        p2_idx = tournament_select(population, fitness, t)
        p1, p2 = population[p1_idx], population[p2_idx]

        c1, c2 = crossover_genes(p1, p2, pc)
        c1 = mutate_gene(c1, pm, bin_count)
        c2 = mutate_gene(c2, pm, bin_count)

        new_population.append(c1)
        if len(new_population) < len(population):
            new_population.append(c2)

    return new_population

# 6. If a termination criterion has been reached, then stop. Otherwise return to step 2.
def run_ga(weights, bin_count, p=100, pm=0.01, t=3, pc=0.8, max_evals=10_000, seed=None):
    if seed is not None:
        random.seed(seed); np.random.seed(seed)

    population = initialize_population(bin_count, weights, population_size=p)
    fitness = evaluate_population(population, bin_count, weights)
    evals = len(population)

    best_idx = np.argmax(fitness)
    best_fit = fitness[best_idx]
    best_sol = population[best_idx].copy()

    while evals < max_evals:
        population = generate_new_population(population, fitness, bin_count, t, pm, pc)
        fitness = evaluate_population(population, bin_count, weights)
        evals += len(population)

        bi = np.argmax(fitness)
        if fitness[bi] > best_fit:
            best_fit = fitness[bi]; best_sol = population[bi].copy()

    return best_fit, best_sol

# BPP1 
weight1 = np.arange(1, 501, dtype=np.int64)
bin1 = 10

# BPP2
i = np.arange(1, 501, dtype=np.int64)
weight2 = (i * i) // 2
bin2 = 50

print(run_ga(weight1, bin1))

