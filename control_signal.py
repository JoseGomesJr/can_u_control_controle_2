import numpy as np
from lands_functions import *
from lands_parameters import *

def constrain(val, min_val, max_val):
    return max(min(val, max_val), min_val)

def computeBestDistance(targetX, targetY, positions):
    minDistance = 1000

    for position in positions:
        currentDistance = ((position[0] - targetX) ** 2 + (position[1] - targetY) ** 2)

        if currentDistance < minDistance:
            minDistance = currentDistance

    return minDistance

def computePositions(x, y, U, land, level, testDepth, dt):
    positions = []
    p = np.array([x, y])

    for i in range(testDepth):
        positions.append(p.copy())

        uIndex = i % len(U)
        u = U[uIndex]
        xp = landsFunctions(land, level, p[0], p[1], u)

        p[0] += xp[0]*dt
        p[1] += xp[1]*dt

    return positions

def evaluateFitness(population, x, y, land, level, testDepth, dt, targetX, targetY):
    fitness = np.zeros(len(population))

    for i, individual in enumerate(population):
        positions = computePositions(x, y, individual, land, level, testDepth, dt)
        fitness[i] = computeBestDistance(targetX, targetY, positions)

    return fitness

def selectParents(population, fitness, numParents):
    sortedIndices = np.argsort(fitness)
    parents = population[sortedIndices[:numParents]]

    return parents

def crossover(parents, numOffspring):
    numParents, numGenes = parents.shape
    offspring = np.empty((numOffspring, numGenes))

    for i in range(numOffspring):
        parent1 = parents[i % numParents]
        parent2 = parents[(i+1) % numParents]

        crossoverPoint = np.random.randint(0, numGenes)
        offspring[i, :crossoverPoint] = parent1[:crossoverPoint]
        offspring[i, crossoverPoint:] = parent2[crossoverPoint:]

    return offspring

def mutate(offspring, mutationRate):
    numOffspring, numGenes = offspring.shape

    for i in range(numOffspring):
        for j in range(numGenes):
            if np.random.rand() < mutationRate:
                offspring[i, j] = np.random.uniform(-1, 1)

    return offspring

def optimizeSignal(x, y, land, level, testDepth, dt, targetX, targetY, upperLimit, lowerLimit, populationSize, numGenerations, numParents, mutationRate):
    numGenes = testDepth
    population = np.random.uniform(low=lowerLimit, high=upperLimit, size=(populationSize, numGenes))

    for _ in range(numGenerations):
        fitness = evaluateFitness(population, x, y, land, level, testDepth, dt, targetX, targetY)
        parents = selectParents(population, fitness, numParents)
        offspring = crossover(parents, populationSize - numParents)
        mutated_offspring = mutate(offspring, mutationRate)
        population = np.vstack((parents, mutated_offspring))

    bestIndividual = population[np.argmin(fitness)]
    bestControlSignal = bestIndividual[0]
    return bestControlSignal
