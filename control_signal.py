import numpy as np
from lands_functions import *
from lands_parameters import *
import pyswarms as ps

def constrain(val, min_val, max_val):
    return max(min(val, max_val), min_val)

def computeBestDistance(targetX, targetY, positions):
    minDistance = np.inf

    for position in positions:
        currentDistance = np.sqrt(np.power(position[0] - targetX, 2) + np.power(position[1] - targetY, 2))

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
    if (abs(x)>0.95 or abs(y)>0.95): #Se saiu da tela, tenta voltar para os centro do mapa.
        targetX = 0.0
        targetY = 0.0

    bestControlSignal = evaluateFitness(x, y, land, level, testDepth, dt, targetX, targetY, upperLimit, lowerLimit)
    return bestControlSignal


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

    #w1 = 1
    # w2 = 1
    # w3 = 1
    # w4 = 0.01
    
    cost = computeBestDistance(targetX, targetY, positions) 

    return cost

def cost_function_wrapper(x, kwargs):
    n_particles = x.shape[0]
    cost = [cost_function(x[i], kwargs) for i in range(n_particles)]
    return np.array(cost)


def evaluateFitness(x, y, land, level, testDepth, dt, targetX, targetY, upperLimit, lowerLimit):
    options = {'c1': 0.1, 'c2': 2, 'w':1}
    bounds = ([lowerLimit], [upperLimit])

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

    optimizer = ps.single.GlobalBestPSO(n_particles=testDepth//10, dimensions=1, options=options, bounds = bounds)

    _, pos = optimizer.optimize(cost_function_wrapper, iters=testDepth//10, kwargs= params)

    u = pos
    return u[0]