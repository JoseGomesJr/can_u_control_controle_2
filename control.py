from math import *
from server_base import Server
import numpy as np

from lands_parameters import *
from control_signal import *

class Control:

  def __init__(self, verbose = False):

    self.verbose = verbose
    self.time = 0
    self.dt = 0.01
    self.controlSignal = 0
    self.previousReceived = []
    self.upperLimit, self.lowerLimit, self.damping, self.testDepth = landsParameters(1, 1)

  def step(self, received):
    if received:
      try:
      
        print(received)

        land, level = received[1], received[2]
        self.upperLimit, self.lowerLimit, self.damping, self.testDepth = landsParameters(land, level)

        player_x, player_y = received[3], received[4]
        target_x, target_y = received[5], received[6]
        if self.previousReceived != received:
          signal = optimizeSignal(player_x, player_y, land, level, self.testDepth, self.dt, target_x, target_y, self.upperLimit, self.lowerLimit, 20, 20, 4, 0.1)
          print(signal)
          self.controlSignal = self.damping*self.controlSignal + (1 - self.damping)*signal
          self.controlSignal = constrain(self.controlSignal, self.lowerLimit, self.upperLimit)

        else:
          self.controlSignal = 0
        
        self.time += self.dt
        self.previousReceived = received
        print("-------", self.controlSignal)
        return self.controlSignal

      except Exception as e:
        print('Error in control step')
        print(str(e))
        pass
      
    # return 0


if __name__=='__main__':
  control = Control()
  server = Server(control)
  server.run()