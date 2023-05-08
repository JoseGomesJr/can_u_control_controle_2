from math import *
import numpy as np

def landsParameters(land, level):
  upperLimit = 1
  lowerLimit = -1
  testDepth = 100

  # LinearLand
  if land == 1:
    damping = 0.65
    if level == 1:
      damping = 0.4
    if level == 3:
      upperLimit = 0.7
      lowerLimit = -0.7
      damping = 0.001
    if level == 4:
      damping = 0.25
  # Non-linearLand
  elif land == 2:
    damping = 0.65
    if level == 3:
          damping = 0.01
    if level == 4:
      damping = 0.35
  # SwitchingLand
  elif land == 3:
    damping = 0.4
    upperLimit = 0.40
    lowerLimit = -0.40
    if level == 2:
      upperLimit = 0.40
      lowerLimit = -0.40
    elif level == 3:
      upperLimit = 0.2
      lowerLimit = -0.2
      damping = 0.2
    elif level == 4:
      upperLimit = 0.7
      lowerLimit = -0.20
  # QuantizedLand
  elif land == 4:
    damping = 0.7
    if level == 3:
      testDepth = 70
      damping = 0.1
  
  return upperLimit, lowerLimit, damping, testDepth