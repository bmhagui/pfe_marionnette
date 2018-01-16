import zmq
import time
import sys


class server :

  def __init__(self):
    
    self.port = "5556"
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.PUB)
    self.socket.setsockopt(zmq.SNDHWM, 3)
    self.socket.bind("tcp://*:%s" % self.port)
    print("Server_Simulation_Step1 initialized")


  def sendDirection(self,length):
    
    return self.socket.send(length) 