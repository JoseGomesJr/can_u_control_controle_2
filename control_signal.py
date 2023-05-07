import numpy as np
from lands_functions import *
from lands_parameters import *
import pyswarms as ps

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

def optimizeSignal(x, y, land, level, testDepth, dt, targetX, targetY, upperLimit, lowerLimit, populationSize, numGenerations, numParents, mutationRate):
    numGenes = testDepth
    population = np.random.uniform(low=lowerLimit, high=upperLimit, size=(populationSize, numGenes))

    bestControlSignal = evaluateFitness(population, x, y, land, level, testDepth, dt, targetX, targetY)
    return bestControlSignal


computePositions

def cost_function(control, params):
    u = control

    x = params.get("x")
    y = params.get("y")
    land = params.get("land")
    level = params.get("level")
    dt = params.get("dt")
    targetX = params.get("targetX")
    targetY = params.get("targetY")
    testDepth = params.get("testDepth")

    positions = computePositions(x, y, [u], land, level, testDepth, dt)

    # w1 = 1
    # w2 = 1
    # w3 = 1
    # w4 = 0.01
    
    cost = computeBestDistance(targetX, targetY, positions)

    return cost

def cost_function_wrapper(x, kwargs):
    n_particles = x.shape[0]
    cost = [cost_function(x[i], kwargs) for i in range(n_particles)]
    return np.array(cost)


def evaluateFitness(population, x, y, land, level, testDepth, dt, targetX, targetY):
    options = {'c1': 0.3, 'c2': 0.9, 'w':0.8}
    bounds = ([-1], [1])

    params = {
        "x": x,
        "y": y,
        "land": land,
        "level": level,
        "dt": dt,
        "targetX": targetX,
        "targetY": targetY,
        "testDepth": testDepth
    }

    optimizer = ps.single.GlobalBestPSO(n_particles=len(population)//10, dimensions=1, options=options, bounds = bounds)

    _, pos = optimizer.optimize(cost_function_wrapper, iters=testDepth//10, kwargs= params)

    u = pos
    return u[0]