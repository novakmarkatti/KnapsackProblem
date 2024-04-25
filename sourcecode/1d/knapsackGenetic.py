import random

def generatePopulation(size, capacity, weights, values, n):
    population, fitnessValues = [], []
    for _ in range(0, size):
        acceptable = False
        while not acceptable:
            chromosome = []
            for _ in range(0, n):
                chromosome.append(random.choice([0, 1]))
            fitness = calculateFitness(capacity, weights, values, chromosome)
            if fitness != 0:
                acceptable = True
                fitnessValues.append(fitness)
        population.append(chromosome)
    return population, fitnessValues

def calculateFitness(capacity, weights, values, chromosome):
    maxValue, maxWeight = 0, 0
    for i in range(0, len(chromosome)):
        if chromosome[i] == 1:
            maxWeight += weights[i]
            maxValue  += values[i]
    if maxWeight > capacity:
        return 0
    else:
        return maxValue
    
def getBestChromosome(population, fitnessValues, weights, values):
    maxFitness = max(fitnessValues)
    maxIndex = fitnessValues.index(maxFitness)
    bestChromosome = population[maxIndex]
    maxValue, maxWeight, selectedItems = 0, 0, []
    for i in range(0, len(bestChromosome)):
        if bestChromosome[i] == 1:
            maxWeight += weights[i]
            maxValue  += values[i]
            selectedItems.append(i+1)
    return maxValue, maxWeight, selectedItems

# REFRESH POPULATION STRATEGYS
def refreshPopulationElitist(child1, child2, population, fitnessValues, capacity, weights, values):
    fitnessChild1 = calculateFitness(capacity, weights, values, child1)
    fitnessChild2 = calculateFitness(capacity, weights, values, child2)
    fitnessTuples = list(enumerate(fitnessValues))
    fitnessTuples.sort(reverse=True, key=lambda value: value[1])
    indexChild1, indexChild2 = fitnessTuples[-1][0], fitnessTuples[-2][0]

    tempPopulation = population.copy()
    tempFitnessValues = fitnessValues.copy()
    tempPopulation[indexChild1]    , tempPopulation[indexChild2]     = child1, child2
    tempFitnessValues[indexChild1] , tempFitnessValues[indexChild2]  = fitnessChild1, fitnessChild2
    return tempPopulation, tempFitnessValues

def refreshPopulationRandomly(child1, child2, population, fitnessValues, capacity, weights, values):
    fitnessChild1 = calculateFitness(capacity, weights, values, child1)
    fitnessChild2 = calculateFitness(capacity, weights, values, child2)
    indexChild1, indexChild2 = random.sample(range(0, len(population)), 2)

    tempPopulation = population.copy()
    tempFitnessValues = fitnessValues.copy()
    tempPopulation[indexChild1]    , tempPopulation[indexChild2]     = child1, child2
    tempFitnessValues[indexChild1] , tempFitnessValues[indexChild2]  = fitnessChild1, fitnessChild2
    return tempPopulation, tempFitnessValues
    
# SELECT STRATEGYS
def selectChromosomesRankbased(population, fitnessValues):
    fitnessTuples = list(enumerate(fitnessValues))
    fitnessTuples.sort(key=lambda value: value[1])
    ranks = [i+1 for i in range(0, len(fitnessTuples))]
    sumRanks = sum(ranks)
    probabilities = [rank / sumRanks for rank in ranks]
    oldIndexes = [i for i, _ in fitnessTuples]
    parent1 = random.choices(oldIndexes, weights=probabilities, k=1)[0]
    parent2 = random.choices(oldIndexes, weights=probabilities, k=1)[0]
    return population[parent1], population[parent2]

def selectChromosomesRouletteWheel(population, fitnessValues):
    probabilities = [f / sum(fitnessValues) for f in fitnessValues]
    parent1 = random.choices(population, weights=probabilities, k=1)[0]
    parent2 = random.choices(population, weights=probabilities, k=1)[0]
    return parent1, parent2

def selectChromosomesTournament(population, fitnessValues, tournamentSize=3):
    parent1 = max(random.sample(list(zip(population, fitnessValues)), tournamentSize), key=lambda x: x[1])[0]
    parent2 = max(random.sample(list(zip(population, fitnessValues)), tournamentSize), key=lambda x: x[1])[0]
    return parent1, parent2

# CROSSOVER STRATEGYS
def crossoverOnePoint(parent1, parent2, crossoverProbability):
    child1, child2 = parent1.copy(), parent2.copy()
    if random.random() < crossoverProbability:
        point1 = random.randint(1, len(parent1) - 2)
        child1 = parent1[:point1] + parent2[point1:]
        child2 = parent2[:point1] + parent1[point1:]
    return child1, child2

def crossoverTwoPoint(parent1, parent2, crossoverProbability):
    child1, child2 = parent1.copy(), parent2.copy()
    if random.random() < crossoverProbability:
        point1 = random.randint(1, len(parent1) - 2)
        point2 = random.randint(1, len(parent1) - 2)
        if point1 > point2:
            point1, point2 = point2, point1
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

# MUTATE STRATEGYS
def mutateBitFlip(chromosome, mutationProbability):
    if random.random() < mutationProbability:
        mutationPoint = random.randint(0, len(chromosome) - 1)
        chromosome[mutationPoint] = 1 - chromosome[mutationPoint]
    return chromosome

def mutateBitSwap(chromosome, mutationProbability):
    if random.random() < mutationProbability:
        point1, point2  = random.sample(range(0, len(chromosome)), 2)
        chromosome[point1], chromosome[point2] = chromosome[point2], chromosome[point1]
    return chromosome

def mutateBitAll(chromosome, mutationProbability):
    for i in range(0, len(chromosome)):
        if random.random() < mutationProbability:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# MAIN FUNCTION
def knapsackGenetic(capacity, weights, values, n, generations=100, populationSize=100, crossoverProbability=0.7, mutationProbability=0.3):
    # 0. initialize population & 1. fitness evaluation
    population, fitnessValues = generatePopulation(populationSize, capacity, weights, values, n)
    for _ in range(generations):
        # 2. select chromosomes 
        parent1, parent2 = selectChromosomesRankbased(population, fitnessValues)
        # 3. crossover
        child1, child2 = crossoverOnePoint(parent1, parent2, crossoverProbability)
        # 4. mutation
        child1 = mutateBitFlip(child1, mutationProbability)
        child2 = mutateBitFlip(child2, mutationProbability)
        # 5. refresh population & 1. update fitness values
        population, fitnessValues = refreshPopulationElitist(child1, child2, population, fitnessValues, capacity, weights, values)
    # 6. final evaluation
    return getBestChromosome(population, fitnessValues, weights, values)



########################################## KISERLET ########################################## 
import time 
import itertools
import knapsackGreedy
import knapsackDP
import json
#population, fitnessValues = generatePopulation(populationSize, capacity, weights, values, n)

# selectChromosomes = (0, "selectChromosomesRankbased"), (1,"selectChromosomesRouletteWheel"), (2, "selectChromosomesTournament")
def selectChromosomes(number, population, fitnessValues):
    if number == 0:
        return selectChromosomesRankbased(population, fitnessValues)
    elif number == 1:
        return selectChromosomesRouletteWheel(population, fitnessValues)
    elif number == 2:
        return selectChromosomesTournament(population, fitnessValues)

# crossover = (0, "crossoverOnePoint"), (1,"crossoverTwoPoint")
def crossover(number, parent1, parent2, crossoverProbability):
    if number == 0:
        return crossoverOnePoint(parent1, parent2, crossoverProbability)
    elif number == 1:
        return crossoverTwoPoint(parent1, parent2, crossoverProbability)

# mutate = (0, "mutateBitFlip"), (1,"mutateBitSwap"), (2, "mutateBitAll")
def mutate(number, chromosome, mutationProbability):
    if number == 0:
        return mutateBitFlip(chromosome, mutationProbability)
    elif number == 1:
        return mutateBitSwap(chromosome, mutationProbability)
    elif number == 2:
        return mutateBitAll(chromosome, mutationProbability)
    
# refreshPopulation = (0, "refreshPopulationElitist"), (1,"refreshPopulationRandomly")
def refreshPopulation(number, child1, child2, population, fitnessValues, capacity, weights, values):
    if number == 0:
        return refreshPopulationElitist(child1, child2, population, fitnessValues, capacity, weights, values)
    elif number == 1:
        return refreshPopulationRandomly(child1, child2, population, fitnessValues, capacity, weights, values)    
        
def knapsackGeneticGeneral(capacity, weights, values, n, combo, population, fitnessValues, generations=100, populationSize=100, crossoverProbability=0.7, mutationProbability=0.3):
    for _ in range(generations):
        # 2. select chromosomes 
        parent1, parent2 = selectChromosomes(combo[0], population, fitnessValues)
        # 3. crossover
        child1, child2 = crossover(combo[1], parent1, parent2, crossoverProbability)
        # 4. mutation
        child1 = mutate(combo[2], child1, mutationProbability)
        child2 = mutate(combo[2], child2, mutationProbability)
        # 5. refresh population & 1. update fitness values
        population, fitnessValues = refreshPopulation(combo[3], child1, child2, population, fitnessValues, capacity, weights, values)
    # 6. final evaluation
    return getBestChromosome(population, fitnessValues, weights, values)

def getCombinations():
    range1 = range(0, 3)  
    range2 = range(0, 2) 
    range3 = range(0, 3) 
    range4 = range(0, 2) 
    combinations = list(itertools.product(range1, range2, range3, range4))
    return combinations

def calculateRelativeError(optimalValue, value):
    relativeError = abs(optimalValue - value) / optimalValue * 100
    return relativeError

def calculateAverageRelativeError(relativeErrors):
    totalErrors = sum(relativeErrors)
    averageError = totalErrors / len(relativeErrors)
    return 100 - averageError


def generatePopulationGreedy(size, capacity, weights, values, n):
    greedySolution = []
    for _ in range(0, n):
        greedySolution.append(0)
    maxValue, maxWeight, selectedItems = knapsackGreedy(capacity, weights, values, n) 
    for i in range(0, len(selectedItems)):  
        greedySolution[ selectedItems[i] - 1 ] = 1

    population, fitnessValues = [], []
    population.append(greedySolution)
    fitness = calculateFitness(capacity, weights, values, greedySolution)
    fitnessValues.append(fitness)
    for _ in range(0, size - 1):
        acceptable = False
        while not acceptable:
            chromosome = []
            for _ in range(0, n):
                chromosome.append(random.choice([0, 1]))
            fitness = calculateFitness(capacity, weights, values, chromosome)
            if fitness != 0:
                acceptable = True
                fitnessValues.append(fitness)
        population.append(chromosome)
    return population, fitnessValues
# -------------------------------------------------- TESZT ----------------------------------------------
inputFile = open('test014.json')
jsonArray = json.load(inputFile)

results = []
combinations = getCombinations()
#percentage = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] 
for test in jsonArray:
    testNumber    = test['testNumber']
    note          = test['note']
    capacity      = test['capacity']
    numberOfItems = test['numberOfItems']
    weights       = test['weights']
    values        = test['values']

    if testNumber == 19 or testNumber == 94:
        continue
    print("#testNumber", testNumber)
    result = []
    # DP
    startTimeDP = time.time()
    maxValueDP, maxWeightDP, selectedItemsDP = knapsackDP(capacity, weights, values, numberOfItems)
    endTimeDP = time.time() - startTimeDP
    result.append((testNumber, endTimeDP, maxValueDP, maxWeightDP, selectedItemsDP, 0))

    # Genetic
    generations, populationSize = 100, 500
    crossoverProbability, mutationProbability = 0.9, 0.3
    population, fitnessValues = generatePopulationGreedy(populationSize, capacity, weights, values, numberOfItems)
    for combo in combinations:
        startTime = time.time()
        maxValue, maxWeight, selectedItems = knapsackGeneticGeneral(capacity, weights, values, numberOfItems, combo, population, fitnessValues, generations, populationSize, crossoverProbability, mutationProbability)
        endTime = time.time() - startTime
        relativeError = calculateRelativeError(maxValueDP, maxValue)
        result.append((testNumber, endTime, maxValue, maxWeight, selectedItems, relativeError))

    results.append(result)

print("###################################")
tuples = []
for i in range(0, len(results[0])):
    endTime = [result[i][1] for result in results]
    realEndTime = sum(endTime) / len(endTime)

    relativeErrors = [result[i][-1] for result in results]
    output = calculateAverageRelativeError(relativeErrors)
    if i == 0:
        tuples.append((i, "DP",           output, realEndTime * 1000))
    elif i>0:
        tuples.append((i, combinations[i-1], output, realEndTime * 1000))

sortedTuples = sorted(tuples, key=lambda x: x[2], reverse=True)
for i in range(0, len(sortedTuples)):
    print(sortedTuples[i])