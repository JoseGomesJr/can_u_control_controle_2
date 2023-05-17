import numpy as np
from lands_functions import *
from lands_parameters import *
import pyswarms as ps

def constrain(val, min_val, max_val):
    return max(min(val, max_val), min_val)

def computeBestDistance(targetX, targetY, positions):
    minDistance = np.inf
    add_cost = 1
    for position in positions:
        currentDistance = np.sqrt(np.power(position[0] - targetX, 2) + np.power(position[1] - targetY, 2))

        if abs(position[0]) > 0.8 or abs(position[1] > 0.8):
            add_cost = 100000

        if currentDistance < minDistance:
            minDistance = currentDistance

    return minDistance*add_cost

def computePositions(x, y, U, land, level, testDepth, dt, signal_actual, damping):
    positions = []
    p = np.array([x, y])

    for i in range(testDepth):
        positions.append(p.copy())

        uIndex = i % len(U)
        u = U[uIndex]
        u = signal_actual + damping[uIndex] * u
        xp = landsFunctions(land, level, p[0], p[1], u)
        
        p[0] += xp[0]*dt
        p[1] += xp[1]*dt

    return positions

def optimizeSignal(x, y, land, level, testDepth, dt, targetX, targetY, upperLimit, lowerLimit, populationSize, numGenerations, numParents, mutationRate, signal_actual, damping):
    bestControlSignal, damping = evaluateFitness(x, y, land, level, testDepth, dt, targetX, targetY, upperLimit, lowerLimit, signal_actual, damping)
    return bestControlSignal, damping


def cost_function(control, params):
    u = control[0]
    damping = control[1]

    x = params.get("x")
    y = params.get("y")
    land = params.get("land")
    level = params.get("level")
    dt = params.get("dt")
    targetX = params.get("targetX")
    targetY = params.get("targetY")
    testDepth = params.get("testDepth")
    signal_actual = params.get("signal_actual")

    positions = computePositions(x, y, [u], land, level, testDepth, dt, signal_actual, [damping])

    #w1 = 1
    # w2 = 1
    # w3 = 1
    # w4 = 0.01
    
    cost = computeBestDistance(targetX, targetY, positions)
    return cost

def cost_function_wrapper(x, kwargs):

    n_particles = x.shape[0]
    cost = [cost_function(x[i],kwargs) for i in range(n_particles)]
    return np.array(cost)


def evaluateFitness(x, y, land, level, testDepth, dt, targetX, targetY, upperLimit, lowerLimit, signal_actual, damping):
    options = {'c1': 0.1, 'c2': 2, 'w':1}
    bounds = ([-10, lowerLimit], [10, upperLimit])

    params = {
        "x": x,
        "y": y,
        "land": land,
        "level": level,
        "dt": dt,
        "targetX": targetX,
        "targetY": targetY,
        "testDepth": testDepth,
        "signal_actual": signal_actual,
        "damping": damping
    }

    optimizer = ps.single.GlobalBestPSO(n_particles=testDepth//10, dimensions=2, options=options, bounds = bounds)

    _, pos = optimizer.optimize(cost_function_wrapper, iters=testDepth//10, kwargs= params)

    print("certo")

    print(_)
    u = pos[0]
    damping = pos[1]

    print(pos)

    return u, damping